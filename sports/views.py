from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import CreateView,DetailView
from .models import Item, Sport,Court,Slot, UserBooking
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

# Create your views here.

class SportCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Sport
    fields = ['name','description','image']

    def test_func(self):
        if self.request.user.type == 2:
            return True
        return False

@login_required
def sportdetail(request,sportid):
    sport = Sport.objects.filter(pk=sportid).first()
    courts = Court.objects.filter(sport=sport)
    inventory = Item.objects.filter(sport=sport)
    return render(request,"sports/sportdetail.html",{'sport':sport,'courts':courts,'inventory':inventory})


class CourtCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Court
    fields = ['name','capacity','image']

    def test_func(self):
        if self.request.user.type == 2:
            return True
        return False

    def form_valid(self, form):
        sportid = self.kwargs["sportid"]
        sport = Sport.objects.filter(pk=sportid).first()
        form.instance.sport = sport
        return super().form_valid(form)

class ItemCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Item
    fields = ['name','number','image']

    def test_func(self):
        if self.request.user.type == 2:
            return True
        return False

    def form_valid(self, form):
        sportid = self.kwargs["sportid"]
        sport = Sport.objects.filter(pk=sportid).first()
        form.instance.sport = sport
        return super().form_valid(form)

@login_required
def courtdetail(request,courtid):
    court = Court.objects.filter(pk=courtid).first()

    if request.method == 'POST':
        if request.user.type == 2:
            datebeforesplit = request.POST['date']
            startbeforesplit = request.POST['starttime']
            endbeforesplit = request.POST['endtime']
            if datebeforesplit and startbeforesplit and endbeforesplit:
                date = datebeforesplit.split('-')
                starttime = startbeforesplit.split(':')
                endtime = endbeforesplit.split(':')
                startdateobject = datetime(int(date[0]),int(date[1]),int(date[2]),int(starttime[0]),int(starttime[1]),0)
                enddateobject = datetime(int(date[0]),int(date[1]),int(date[2]),int(endtime[0]),int(endtime[1]),0)
                slot = Slot(start=startdateobject,end=enddateobject,court=court,avail=court.capacity)
                slot.save()
            else:
                messages.warning(request,'fill all the fields!')
        else:
            slotid = request.POST['slot']
            slot = Slot.objects.filter(pk=slotid).first()
            dayoldtime = timezone.now()-timedelta(days=1)
            thisdaybooks = UserBooking.objects.filter(user=request.user,booking_time__gte=dayoldtime).count()
            if slot.avail > 0 and thisdaybooks < 3:
                booking = UserBooking(user=request.user,slot=slot,status=1)
                booking.save()
                slot.avail -= 1
                slot.save()
                messages.success(request, 'Your booking has been accepted!. Check Profile to see all actions! All Updates will be notified by email!')
            else:
                booking = UserBooking(user=request.user,slot=slot,status=0)
                booking.save()
                messages.success(request, 'Your booking has been rejected!. Check Profile to see all actions! All Updated will be notified by email!')
    
    bookingclosetime = timezone.now() + timedelta(hours=3)
    slots = Slot.objects.filter(court=court,avail__gte=1,start__gte=bookingclosetime)
    context = {'court':court,'slots':slots}
    return render(request,"sports/courtdetail.html",context)




