import re
import sqlite3

from django.shortcuts import render
from django.http import HttpResponseRedirect

# Must be passed a list of skill ids
def fit_score(job_offer_skill_ids: tuple[int]) -> int:
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
    skill_ids = ','.join("?" for _ in job_offer_skill_ids)
    cursor.execute(f'select count(skill_id) from my_skill where skill_id in ({skill_ids})', job_offer_skill_ids)
    
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
            if job_id == '':
                job_id = 'N/A'
                print(f'Job ID not given.')
            '''
            print(f'job id: {job_id}')
            print('\n')
            '''
            
            position = request.POST.get('position')
            '''
            print(f'position: {position}')
            print('\n')
            '''
            
            date_posted = request.POST.get('date_posted')
            print(f'Date posted: {date_posted}')
            
            # Extracts information about the job
            about_the_job = request.POST.get('about_the_job')
            about_the_job_details = []
            if about_the_job == '':
                about_the_job = 'N/A'
                about_the_job_details = ['N/A']
                print(f'Job description not given.')
            else:
                about_the_job_details = about_the_job.split('\n')
                about_the_job_details = [' '.join(about_the_job_detail.split()[1:]) for about_the_job_detail in about_the_job_details]
                '''
                print('about the job:')
                for about_the_job_detail in about_the_job_details:
                    print(f'\t{about_the_job_detail}')
                print('\n')
                '''
            
            location = request.POST.get('location')
            '''
            print(f'location: {location}')
            print('\n')
            '''
            
            salary = request.POST.get('salary')
            if salary == '':
                salary = 'N/A'
                print(f'Salary not given.')
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
            '''
            print(results)
            '''
            
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
            score = fit_score(tuple(job_offer_skill_ids))
            #print(f'fit_score of job offer: {score}')
            
            benefits = request.POST.get('benefits')
            if benefits == '':
                benefits = 'N/A'
            #    print(f'Benefits not given.')
            else:
                benefits = benefits.split('\n')
                benefits = [' '.join(benefit.split()[1:]) for benefit in benefits]
                '''
                print('benefits:')
                print(f'\n{benefits}')
                print('\n')
                '''
            ######## Add job offer ########
            cursor = conn.execute(f'insert into job_offer(company, job_id, position, location, salary, date_posted, application_status, fit_score) values (?,?,?,?,?,?,?,?)', (company_name, job_id, position, location, salary, date_posted, 'N/A', score))
            conn.commit()
            job_offer_id = cursor.lastrowid
            '''
            print(f'Job offer added.')
            print(f'ID: {job_offer_id}')
            '''
            
            ######## Adding job offer's description details ########
            if len(about_the_job_details) == 1 and about_the_job_details[0] == 'N/A':
                cursor = conn.execute(f'insert into job_description_bullet(job_offer_id, description_bullet) values (?,?)', (job_offer_id, 'N/A'))
                conn.commit()
            else:
                cursor = conn.executemany(f'insert into job_description_bullet(job_offer_id, description_bullet) values(?,?)', list(zip([job_offer_id] * len(about_the_job_details), about_the_job_details)))
                conn.commit()
            '''
            cursor = conn.execute(f'select * from job_description_bullet where job_offer_id = (?)', [job_offer_id])
            results = cursor.fetchall()
            print(f'Job Description Bullet Results:')
            for result in results:
                print(f'\t{result[0]}, {result[1]}, {result[2]}')
            '''
                
            ######## Adding job offer's responsibilities ########
            cursor = conn.executemany(f'insert into job_responsibility(job_offer_id, responsibility) values(?,?)', list(zip([job_offer_id] * len(responsibilities), responsibilities)))
            conn.commit()
            '''
            cursor = conn.execute(f'select * from job_responsibility where job_offer_id = (?)', [job_offer_id])
            results = cursor.fetchall()
            print(f'Job Responsibilities:')
            for result in results:
                print(f'\t{result[0]}, {result[1]}, {result[2]}')
            '''
                
            ######## Adding job offer's requirements ########
            cursor = conn.executemany(f'insert into job_requirement(job_offer_id, requirement) values(?,?)', list(zip([job_offer_id] * len(requirements), requirements)))
            conn.commit()
            '''
            cursor = conn.execute(f'select * from job_requirement where job_offer_id = (?)', [job_offer_id])
            results = cursor.fetchall()
            print(f'Job Requirements:')
            for result in results:
                print(f'\t{result[0]}, {result[1]}, {result[2]}')
            '''
                
            ######## Adding job offer's benefits ########
            print(f'benefits: {benefits}')
            if type(benefits) == str:
                cursor = conn.execute(f'insert into job_benefit(job_offer_id, benefit) values(?,?)', (job_offer_id, 'N/A'))
                conn.commit()
                #print(f'\tN/A saved for benefits.')
            else:
                cursor = conn.executemany(f'insert into job_benefit(job_offer_id, benefit) values(?,?)', list(zip([job_offer_id] * len(benefits), benefits)))
                conn.commit()
                #print(f'\tMany benefits added.')
            '''
            cursor = conn.execute(f'select * from job_benefit where job_offer_id = (?)', [job_offer_id])
            results = cursor.fetchall()
            print(f'Job Benefits:')
            for result in results:
                print(f'\t{result[0]}, {result[1]}, {result[2]}')
            '''
                
            ######## Adding job offer's skill_ids ########
            cursor = conn.executemany(f'insert into job_offer_skill(job_offer_id, skill_id) values(?,?)', list(zip([job_offer_id] * len(job_offer_skill_ids), job_offer_skill_ids)))
            conn.commit()
            #cursor = conn.execute(f'select skill_id from job_offer_skill where job_offer_id = (?)', [job_offer_id])
            #results = cursor.fetchall()
            #skill_ids = [result[0] for result in results]
            #placeholder = ','.join('?' for _ in job_offer_skill_ids)
            '''
            cursor = conn.execute(f'select id, name from skill where id in ({placeholder})', list(job_offer_skill_ids))
            results = cursor.fetchall()
            print(f'Gathered Job Offer Skills:')
            for result in results:
                print(f'\tID: {result[0]} Name: {result[1]}')
            '''
        elif action == 'update_job_offer':
            job_posting_sql_id = request.POST.get('sql_id')
            #print(f'job offer sql id": {job_posting_sql_id}')
            job_posting_status = request.POST.get('job_status').lower()
            #print(f'job offer status: {job_posting_status}')
            conn = sqlite3.connect('/Users/stevencrowther/Documents/Coding/web development/job_search-root/db.sqlite3')
            cursor = conn.cursor()
            cursor.execute(f'update job_offer set application_status = ? where id = ?', (job_posting_status, job_posting_sql_id))
            conn.commit()
        elif action == 'cancel_job_offer':
            pass
        
        #return HttpResponseRedirect('/')
    
    connection = sqlite3.connect('/Users/stevencrowther/Documents/Coding/web development/job_search-root/db.sqlite3')
    cursor = connection.cursor()
    
    cursor.execute('select id, company, job_id, position, location, salary, date_posted, date_applied, application_status, fit_score from job_offer')
    job_offer_results = cursor.fetchall()
    job_offers = {}
    for job_offer_result in job_offer_results:
        job_offers[job_offer_result[0]] = {
            'sql_id' : job_offer_result[0],
            'company' : job_offer_result[1],
            'job_id' : job_offer_result[2],
            'position' : job_offer_result[3],
            'location' : job_offer_result[4],
            'salary' : job_offer_result[5],
            'date_posted' : job_offer_result[6],
            'date_applied' : job_offer_result[7],
            'application_status' : job_offer_result[8],
            'fit_score' : job_offer_result[9],
            'description' : [],
            'responsibilities' : [],
            'requirements' : [],
            'benefits' : [],
            'skills' : [],
            'my_skills' : []
        }
    cursor.execute('select id, name from skill')
    skill_results = cursor.fetchall()
    skill_results = { skill_result[0] : skill_result[1] for skill_result in skill_results }

    
    cursor.execute('select job_offer_id, skill_id from job_offer_skill')
    job_offer_skill_results = cursor.fetchall()
    
    cursor.execute('select id, skill_id from my_skill')
    my_skill_results = cursor.fetchall()
    my_skill_set = set(my_skill_result[1] for my_skill_result in my_skill_results)
    
    #print(f'My skill ids {my_skill_set}')
    #print(job_offer_skill_results)
    '''
    print(f'My matching skills for:')
    print(f'\tjob offer: {job_offer_result[0]}')
    print(f'\tcompany: {job_offer_result[1]}')
    print(f'\tposition: {job_offer_result[3]}')
    '''
    for job_offer_skill_result in job_offer_skill_results:
        '''
        if 'skills' not in job_offers[job_offer_skill_result[0]].keys():
            job_offers[job_offer_skill_result[0]]['skills'] = [skill_results[job_offer_skill_result[1]]]
        else:
        '''
        job_offers[job_offer_skill_result[0]]['skills'].append(skill_results[job_offer_skill_result[1]])
        
        # Displays my skills that are also job posting skills
        if job_offer_skill_result[1] in my_skill_set:
            #print(f'\t\t{skill_results[job_offer_skill_result[1]]}')
            job_offers[job_offer_skill_result[0]]['my_skills'].append(skill_results[job_offer_skill_result[1]])
    
    cursor.execute('select id, job_offer_id, benefit from job_benefit')
    job_benefit_results = cursor.fetchall()
    for job_benefit_result in job_benefit_results:
        '''
        if 'benefits' not in job_offers[job_benefit_result[1]].keys():
            job_offers[job_benefit_result[1]]['benefits'] = [job_benefit_result[2]]
        else:
        '''
        job_offers[job_benefit_result[1]]['benefits'].append(job_benefit_result[2])
    
    cursor.execute('select id, job_offer_id, description_bullet from job_description_bullet')
    job_description_bullet_results = cursor.fetchall()
    for job_description_bullet_result in job_description_bullet_results:
        '''
        if 'description' not in job_offers[job_description_bullet_result[1]].keys():
            job_offers[job_description_bullet_result[1]]['description'] = [job_description_bullet_result[2]]
        else:
        '''
        job_offers[job_description_bullet_result[1]]['description'].append(job_description_bullet_result[2])
    
    cursor.execute('select id, job_offer_id, requirement from job_requirement')
    job_requirement_results = cursor.fetchall()
    #print('Requirements:')
    #print(job_requirement_results)
    for job_requirement_result in job_requirement_results:
        '''
        if 'requirement' not in job_offers[job_requirement_result[1]].keys():
            job_offers[job_requirement_result[1]]['requirement'] = [job_requirement_result[2]]
        else:
        '''
        #print(f'job offer id: {job_requirement_result[2]}')
        job_offers[job_requirement_result[1]]['requirements'].append(job_requirement_result[2])
    
    cursor.execute('select id, job_offer_id, responsibility from job_responsibility')
    job_responsibility_results = cursor.fetchall()
    for job_responsibility_result in job_responsibility_results:
        '''
        if 'responsibility' not in job_offers[job_requirement_result[1]].keys():
            job_offers[job_responsibility_result[1]]['responsibility'] = [job_responsibility_result[2]]
        else:
        '''
        job_offers[job_responsibility_result[1]]['responsibilities'].append(job_responsibility_result[2])
    
    job_offers = [job_offer for job_offer in job_offers.values()]
    #print(job_offers)
    context = { "job_postings" : job_offers }
    return render(request, 'myapp/index.html', context)