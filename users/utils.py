from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def searchProfiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skill_list = Skill.objects.filter(name__icontains=search_query)
    print(skill_list)
    profiles = Profile.objects.distinct().filter(
            Q(name__icontains=search_query) |
            Q(short_intro__icontains=search_query) |
            Q(skill__in=skill_list))
        
    return profiles, search_query

   

def paginateProfiles(request,profiles,profile_per_page):
     
    p = Paginator(profiles,profile_per_page)
    page = request.GET.get('page')
    try:
        profiles = p.page(page)
    except PageNotAnInteger:
        page =1
        profiles = p.page(page)
    except EmptyPage:
        page = p.num_pages
        profiles = p.page(page)

    
    leftIndex = int(page)-4
    if leftIndex<1:
        leftIndex=1

    
    rightIndex = int(page)+4
    print('right:',rightIndex,'pag_num:',p.num_pages)
    if rightIndex >= p.num_pages:
        rightIndex = p.num_pages +1
    
    print("Total Pages =",p.num_pages)

    custom_range = range(leftIndex,rightIndex)

    return profiles,custom_range