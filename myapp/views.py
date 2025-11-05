import sqlite3

from django.shortcuts import render
from django.http import HttpResponseRedirect

# Must be passed a list of skill ids
def fit_score(job_offer_skill_ids: list[int]) -> int:
    conn = sqlite3.connect('/Users/stevencrowther/Documents/Coding/web development/job_search-root/db.sqlite3')
    cursor = conn.cursor()
    sum = 0
    '''
    # Option 1 start
    for job_offer_skill_id in job_offer_skill_ids:
        # Get skill ids
        #cursor.execute(f'select id from skill where id = "{job_offer_skill_id}"')
        
        #id = cursor.fetchone()[0]
        
        cursor.execute(f'select skill_id from my_skill where skill_id = "{job_offer_skill_id}"')

        if cursor.fetchone():
            sum += 1
        else:
            pass
    # Option 1 end
    '''
    # Option 2 start
    skills = ','.join("?" for _ in job_offer_skill_ids)
    print(job_offer_skill_ids)
    cursor.execute(f'select count(id) from my_skill where skill_id in ({skills})', job_offer_skill_ids)
    sum = cursor.fetchone()[0]
    # Option 2 end
    
    return int((sum / len(job_offer_skill_ids)) * 100)

# Create your views here.
def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        print(f"Received Name: {name}")
        return HttpResponseRedirect('/')
    
    return render(request, 'myapp/index.html')