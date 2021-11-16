from django.shortcuts import render,redirect,get_object_or_404
from .models import Wallet,Transaction,Notification
from users.models import User
from .forms import TransactionForm
from django.contrib import messages
from django.db.models import Q
from datetime import datetime,date
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage









import random
def autoGenerateREF():
    ref_num = ''
    for i in range(0,16):
        ref_num += str(random.randint(0, 9))
    return ref_num

def autoGenerateTRX():
    trx_num = ''
    for i in range(0,16):
        trx_num += str(random.randint(0, 9))
    return trx_num

@login_required
def home(request):
    return render(request,'pay/home.html',{})

@login_required
def walletPage(request):
    user = request.user
    return render(request,'pay/wallet.html',{'user':user})

@login_required
def confirmTransfer(request):
    data = request.session.get('transaction_data')
    
    if data:
        to_user = User.objects.get(phone=data['to_user'])
        amount = data['amount']
        description = data['description']
        print('user:',to_user,'amount:',amount,'description',description)
        

        context = {
            'data':data,
            'to_user':to_user,
            'amount':amount,
            'description':description
            }
        
        # checking confirm
        if request.method == "POST":
            password = request.POST.get('password')
            user = authenticate(request,phone=request.user.phone,password=password)

            # checking password is valid
            if user:
                
                # Sender obj
                from_user = Wallet.objects.get(account_person=request.user)
                
                # test not to equal sender and receiver
                if request.user == to_user:
                    messages.warning(request, "You cannot transfer to yourself!!!")
                    return redirect('transfer')


                del request.session['transaction_data']
                # Check balance
                if int(from_user.amount) >= int(amount):
                    # Reduce money from sender
                    from_user.amount -= int(amount)
                    from_user.save()
                    

                    # Add money to receiver
                    to_user.wallet.amount += int(amount)
                    to_user.wallet.save()

                    # Create Transaction obj for sender
                    ref_no=autoGenerateREF()
                    Transaction.objects.create(
                        ref_no=ref_no,
                        trx_id=autoGenerateTRX(),
                        amount=int(amount), 
                        from_user=request.user, 
                        to_user=to_user, 
                        transfer_type="Expense", 
                        description=description
                    )
                    # Create Transaction obj for receiver
                    Transaction.objects.create(
                        ref_no=ref_no,
                        trx_id=autoGenerateTRX(),
                        amount=int(amount), 
                        from_user=to_user, 
                        to_user=request.user, 
                        transfer_type="Income", 
                        description=description
                    )

                    # Create Noti for sender
                    Notification.objects.create(
                        user = request.user,
                        amount= amount,
                        transfer_type= "Expense",
                        data = f'You have sent {amount} MMK to {to_user.name} '
                        
                    )

                    # Create Noti for receiver
                    Notification.objects.create(
                        user = to_user,
                        amount= amount,
                        transfer_type= "Income",
                        data = f'You have received {amount} MMK from {request.user.name} '
                    )
                    
                    messages.success(request, "Successfully sent")
                    return redirect('home')
                else:
                    messages.warning(request, "Low Balance!")
                    return redirect('transfer')
            else:
                messages.warning(request, "Your password is incorrect!!")
                return render(request,'pay/confirm.html',context)
        else:
            return render(request,'pay/confirm.html',context)   
    else:
        return redirect('transfer')

    
   
@login_required
def transfer(request):
    form = TransactionForm()
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = request.POST.get('amount')
            try:
                # Check receiver's account is created
                print(type(request.POST.get('to_user')))
                
                to_user = User.objects.get(phone=request.POST.get('to_user'))
                print(to_user)
                
                # Use session to pass date to another view
                request.session['transaction_data'] = request.POST
    
                return redirect('confirm')
    
            except Exception:
                messages.warning(request, "Something went wrong!! check this user is valid!!")
           
            
    context = {'form':form}
    return render(request,'pay/transfer.html',context)


@login_required
def notificationPage(request):
    notis_list = Notification.objects.filter(user=request.user)
    page = request.GET.get('page',1)

    paginator = Paginator(notis_list, 8)
    try:
        notis = paginator.page(page)
    except PageNotAnInteger:
        notis = paginator.page(1)
    except EmptyPage:
        notis = paginator.page(paginator.num_pages)

    context = {
        'notis':notis
    }
    return render(request,'pay/notification.html',context)

@login_required
def notificationDetail(request,pk):
    noti = get_object_or_404(Notification,pk=pk)
    if noti.user != request.user:
        return redirect('noti')

    noti.noti_type = "Read"
    noti.save()
    context = {
        'noti':noti
    }
    return render(request,'pay/notificationDetail.html',context)



def transactionsPage(request):
    input_date = request.GET.get('date') if request.GET.get('date') != None else ''
    if input_date == "":
        today = datetime.today()
        input_date = today.strftime("%Y-%m-%d")
    
        
    tran_type = request.GET.get('type') if request.GET.get('type') != None else ''
    

    if tran_type == "Expense":
        transactions = Transaction.objects.filter(
            Q(from_user=request.user) &
            Q(transfer_type="Expense") &
            Q(created__date=input_date)
        )
    elif tran_type == "Income":
        transactions = Transaction.objects.filter(
            Q(from_user=request.user) &
            Q(transfer_type="Income") &
            Q(created__date=input_date)
        )
    else:
        transactions = Transaction.objects.filter(
            Q(from_user=request.user) & 
            Q(created__date=input_date)
        )

   
       
    context = {
        'transactions': transactions
    }
    return render(request,'pay/transactions.html',context)

def transactionDetail(request,pk):
    transaction = get_object_or_404(Transaction,pk=pk)
    if transaction.from_user != request.user:
        return redirect('transactions')
    context = {
        'transaction': transaction
    }
    return render(request,'pay/transactionDetail.html',context)


def scanqr(request):
    return render(request,'pay/scanner.html',{})


import qrcode
import qrcode.image.svg
from io import BytesIO
def receiveQR(request):
    user = request.user
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(user.phone, image_factory=factory, box_size=20)
    stream = BytesIO()
    img.save(stream)
    context = {
        'svg': stream.getvalue().decode()
    }
    

    return render(request,'pay/receiveqr.html',context)