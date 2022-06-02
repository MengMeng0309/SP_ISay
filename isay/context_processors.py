from os import access
from .models import Appointment

def get_summary(request):
    count = Appointment.objects.filter(accepted = True).count()
    count2 = Appointment.objects.filter(gender = "Female").count()
    count3 = Appointment.objects.filter(gender = "Male").count()
    count4 = Appointment.objects.filter(services = "Counseling").count()
    count5 = Appointment.objects.filter(services = "Psychological Testing").count()
    count6 = Appointment.objects.filter(services = "Career Guidance, Graduate Placement and Follow-up").count()
    count7 = Appointment.objects.filter(services = "Human Development Services").count()
    count8 = Appointment.objects.filter(services = "Peer Facilitating Program").count()
    count9 = Appointment.objects.filter(college = "CAS").count()
    count10 = Appointment.objects.filter(college = "SOTECH").count()
    count11 = Appointment.objects.filter(college = "CFOS").count()
    count12 = Appointment.objects.filter(college = "UPVHS").count()
    count13 = Appointment.objects.filter(college = "UPVCT").count()
    count14 = Appointment.objects.filter(college = "CM").count()


    

    data = {
        "accepted_count":count,
        "female_count":count2,
        "male_count":count3,
        "counsel_count":count4,
        "psy_count":count5,
        "car_count":count6,
        "human_count":count7,
        "peer_count":count8,
        "CAS_count":count9,
        "CM_count":count10,
        "SOTECH_count":count11,
        "CFOS_count":count12,
        "UPVHS_count":count13,
        "UPVTC_count":count14,

    }
    return data