import re
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
        #name = request.POST.get('name')
        #print(f"Received Name: {name}")
        action = request.POST.get('action')
        #print(action)
        
        if action == 'add_job_offer':  
            company_name = request.POST.get('company_name')
            '''
            print(f'company name: {company_name}')
            print('\n')
            '''
                        
            job_id = request.POST.get('job_id')
            '''
            print(f'job id: {job_id}')
            print('\n')
            '''
            
            position = request.POST.get('position')
            '''
            print(f'position: {position}')
            print('\n')
            '''
            
            # Extracts information about the job
            about_the_job = request.POST.get('about_the_job')
            if len(about_the_job) != 3:
                about_the_job_details = about_the_job.split('\n')
                about_the_job_details = [' '.join(about_the_job_detail.split()[1:]) for about_the_job_detail in about_the_job_details]
                '''
                print('about the job:')
                for about_the_job_detail in about_the_job_details:
                    print(f'\t{about_the_job_detail}')
                print('\n')
                '''
            else:
                print(f'about the job: {about_the_job}')
            
            location = request.POST.get('location')
            '''
            print(f'location: {location}')
            print('\n')
            '''
            
            salary = request.POST.get('salary')
            '''
            print(f'salary: {salary}')
            print('\n')
            '''

            # Extracts requirements   
            responsibilities = request.POST.get('responsibilities').split('\n')
            responsibilities = [' '.join(responsibility.split()[1:]) for responsibility in responsibilities]
            '''
            print('responsibilities:')
            for responsibility in responsibilities:
                print(f'\t{responsibility}')
            print('\n')
            '''
            
            # Extracts requirements    
            requirements = request.POST.get('requirements').split('\n')
            requirements = [' '.join(requirement.split()[1:]) for requirement in requirements]
            lowercase_requirements = [requirement.lower() for requirement in requirements]
            conn = sqlite3.connect('/Users/stevencrowther/Documents/Coding/web development/job_search-root/db.sqlite3')
            cursor = conn.cursor()
            cursor.execute('select id, lower(name) from skill')
            results = cursor.fetchall()
            #print(results)
            
            job_offer_skill_ids = set()
            print(f'Job Offer Skills:')
            for lowercase_requirement in lowercase_requirements:
                print(f'\t{lowercase_requirement}')
                for id, name in results:
                    #print(f'\tskill name: {name}')
                    '''
                    if name == 'c++':
                        if re.search(r'(?<!\w)c\+\+(?!\w)', lowercase_requirement):
                            job_offer_skill_ids.add(id)
                            print(f'\tskill found:{name}')
                    elif name == 'c#':
                        if re.search(r'(?<!\w)c#(?!\w)', lowercase_requirement):
                            job_offer_skill_ids.add(id)
                            print(f'\tskill found:{name}')
                    elif name == 'f#':
                        if re.search(r'(?<!\w)f#(?!\w)', lowercase_requirement):
                            job_offer_skill_ids.add(id)
                            print(f'\tskill found:{name}')
                    else:
                    '''
                    if re.search(rf'(?<!\w){re.escape(name)}(?!\w)', lowercase_requirement):
                        if id not in job_offer_skill_ids:
                            job_offer_skill_ids.add(id)
                            print(f'\tskill found: {name}')
                        
            benefits = request.POST.get('benefits')
            if len(benefits) != 3:
                benefits = benefits.split('\n')
                benefits = [' '.join(benefit.split()[1:]) for benefit in benefits]
                '''
                print('benefits:')
                print(f'\n{benefits}')
                print('\n')
                '''
            else:
                print(f'\t{benefits}')
            
        elif action == 'update_job_offer':
            pass
        elif action == 'cancel_job_offer':
            pass
        
        return HttpResponseRedirect('/')
    
    return render(request, 'myapp/index.html')