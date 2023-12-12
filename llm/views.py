import requests, json
import re, time, os
import numpy as np
import urllib
import uuid
import inspect
import time, random
from urllib.parse import urlparse
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


import openai
from openai import OpenAI
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.core.mail import mail_admins

from .models import * 

PROBABILITY_MUTATE = 1.0
NUM_CHILDREN = 4
CHATGPT_MODEL = "gpt-4-1106-preview" # "gpt-3.5-turbo" #
DALLE_MODEL = "dall-e-3" # "dall-e-2" # 

fakeuserinputllm = True
fakecrossoverllm = True
fakemutationllm = True
fakeimagegen = True
# fakeimagepromptllm = True

MAX_RUNS_PER_PAGE = 5

if settings.DEBUG == False:
    fakeuserinputllm = False
    fakecrossoverllm = False
    fakemutationllm = False
    fakeimagegen = False
    # fakeimagepromptllm = False

fakellm_delay = 0

client = OpenAI()

keyword_examples = ['architectural style', 'site', 'colors', 'lighting', 'shape/form', 'materials']


# def get_all_runs(request):
#     real_runs = UserInput.objects.exclude(response="fake").exclude(response="").filter(version=1).exclude(hide=True).order_by('-timestamp')
#     for run in real_runs:
#         images = Image.objects.filter(session=run.session).order_by('-instance')[:4][::-1] # get the final 4 instance, sorted in the right order
#         run.images = images
#     return render(request, 'llm/all_runs.html', {
#     'runs': real_runs,
#     })

def get_all_runs(request):
    page = request.GET.get('page', 1)  # Get the current page number from the request parameters

    try:
        page = int(page)
        if page < 1:
            # Redirect to the first page if the page number is less than 1
            return redirect('llm_all_runs')
    except ValueError:
        # Redirect to the first page if the page parameter is not a valid integer
        return redirect('llm_all_runs')


    real_runs = UserInput.objects.exclude(response="fake").exclude(response="").filter(version=1).exclude(hide=True).order_by('-timestamp')

    # Paginate the queryset
    paginator = Paginator(real_runs, MAX_RUNS_PER_PAGE)  # Show 10 runs per page
    try:
        real_runs = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, show the first page
        real_runs = paginator.page(1)
    except EmptyPage:
        # If the page parameter is out of range, show the last page
        real_runs = paginator.page(paginator.num_pages)

    for run in real_runs:
        images = Image.objects.filter(session=run.session).order_by('-instance')[:4][::-1]
        run.images = images

    return render(request, 'llm/all_runs.html', {
        'runs': real_runs,
    })


def get_history(request, uuid_param):
    # try:
    # Use the UUID parameter as needed
    uuid_obj = uuid.UUID(uuid_param)

    # get user input
    user_input = UserInput.objects.filter(session=uuid_obj)[0]


    images = Image.objects.filter(session=uuid_obj).order_by('instance') # order it so that children appear in order

    # get the iteration number of the last image
    last_image = images.last().iteration

    loop_range = last_image + 1

    history = []

    for i in range(loop_range):
        try:
            feedback = UserSelectionFeedback.objects.get(session=uuid_obj, iteration=i)
        except UserSelectionFeedback.DoesNotExist:
            feedback = None

        images = Image.objects.filter(session=uuid_obj, iteration=i).order_by('instance')
        crossover = Crossover.objects.filter(session=uuid_obj, iteration=i)
        mutation = Mutation.objects.filter(session=uuid_obj, iteration=i)
        children = Children.objects.filter(session=uuid_obj, iteration=i)

        for image in images:
            # image_prompt = ImagePrompt.objects.get(session=uuid_obj, instance=image.instance)
            attributes = json.loads(image.attributes)
            image.attributes = attributes

            # attribute_feedback = {}
            # for k in attributes.keys():
            #     attribute_feedback[k] = {}
            #     attribute_feedback[k]["value"] = attributes[k]

            if feedback:
                attribute_feedback = {}
                if feedback.parent1_id == image.instance:
                    for k in attributes.keys():
                        attribute_feedback[k] = {} # 
                        attribute_feedback[k]["value"] = attributes[k] #
                        parent1_feedback_json = json.loads(feedback.parent1_feedback)
                        attribute_feedback[k]["feedback"] = parent1_feedback_json[k]
                    image.role = "Parent 1"
                elif feedback.parent2_id == image.instance:
                    for k in attributes.keys():
                        attribute_feedback[k] = {} #
                        attribute_feedback[k]["value"] = attributes[k] #
                        parent2_feedback_json = json.loads(feedback.parent2_feedback)
                        attribute_feedback[k]["feedback"] = parent2_feedback_json[k]
                    image.role = "Parent 2"

                image.attribute_feedback = attribute_feedback

        iteration = {}
        iteration['images'] = images

        if feedback:
            parent1_iteration = int(feedback.parent1_id.split('-')[0])
            parent2_iteration = int(feedback.parent2_id.split('-')[0])
            if parent1_iteration != i:
                parent_json = json.loads(feedback.parent1_json)
                attribute_feedback = {}
                for k in parent_json.keys():
                    attribute_feedback[k] = {} # 
                    attribute_feedback[k]["value"] = parent_json[k] #
                    parent1_feedback_json = json.loads(feedback.parent1_feedback)
                    attribute_feedback[k]["feedback"] = parent1_feedback_json[k]
                iteration['parent1'] = {}
                iteration['parent1']['id'] = feedback.parent1_id
                iteration['parent1']['iteration'] = parent1_iteration
                iteration['parent1']['attribute_feedback'] = attribute_feedback
                # iteration['parent1']['json'] = json.loads(feedback.parent1_json)
                # iteration['parent1']['feedback'] = json.loads(feedback.parent1_feedback)
            if parent2_iteration != i:
                parent_json = json.loads(feedback.parent2_json)
                attribute_feedback = {}
                for k in parent_json.keys():
                    attribute_feedback[k] = {} # 
                    attribute_feedback[k]["value"] = parent_json[k] #
                    parent2_feedback_json = json.loads(feedback.parent2_feedback)
                    attribute_feedback[k]["feedback"] = parent2_feedback_json[k]
                iteration['parent2'] = {}
                iteration['parent2']['id'] = feedback.parent2_id
                iteration['parent2']['iteration'] = parent2_iteration
                iteration['parent2']['attribute_feedback'] = attribute_feedback
                # iteration['parent1']['json'] = json.loads(feedback.parent1_json)
                # iteration['parent1']['feedback'] = json.loads(feedback.parent1_feedback)


        if mutation:
            iteration['mutation'] = {}
            iteration['mutation']['attributes'] = json.loads(mutation[0].attributes)
            iteration['mutation']['result'] = json.loads(mutation[0].result)
            iteration['mutation']['avoid_values'] = json.loads(mutation[0].avoid_values)
        if crossover:
            iteration['crossover'] = {}
            iteration['crossover']['result'] = json.loads(crossover[0].result)
        if children:
            iteration['children'] = {}
            iteration['children']['children_after_crossover'] = json.loads(children[0].children_after_crossover)
            try: # in case mutation has not been completed
                iteration['children']['children_after_mutation'] = json.loads(children[1].children_after_mutation)
            except:
                pass
        history.append(iteration)
    return render(request, 'llm/history.html', {
        'user_input': user_input,
        'history': history,
        })
    # except Exception as e:
    #     print(e)
    #     return HttpResponse('Invalid UUID format')


# def is_probability_true(value):
#     return (random.uniform(0.0, 1.0) <= value) # the higher value, the more likely to return true


def extract_json(input_text):
    # Check if ```json is present
    if "```json" in input_text:
        # Use regular expression to extract content between ```json and ```
        match = re.search(r'```json(.*?)```', input_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            return input_text.strip()
    else:
        # If ```json is not present, return the entire content
        return input_text.strip()


def is_unwanted(new_value, unwanted_list):
    new_value = new_value.replace(',', ' ').strip()
    for unwanted in unwanted_list:
        unwanted = unwanted.strip()
        if f" {unwanted} " in f" {new_value} " or new_value.startswith(f"{unwanted} ") or new_value.endswith(f" {unwanted}"):
            return True
    return False




def ajax_final_feedback(request):
    response_data = {}

    try:
        session = request.POST.get('session')
        iteration = request.POST.get('iteration')

        user_input = request.POST.get('user_input')

        final_id = request.POST.get('final_id')
        final_json = request.POST.get('final_json')
        final_image = request.POST.get('final_image')
        final_feedback = request.POST.get('final_feedback')

        current_iteration_results = request.POST.get('current_iteration_results')

        comments = request.POST.get('comments')
        contact = request.POST.get('contact')

        FinalFeedback.objects.create(
            session=session,
            iteration=iteration,
            user_input=user_input,
            final_id=final_id,
            final_json=final_json,
            final_image=final_image,
            final_feedback=final_feedback,
            current_iteration_results=current_iteration_results,
            comments=comments,
            contact=contact,
        )

        mail_admins(f"Feedback!", f"user_input: {user_input}\n\nfinal_json: {final_json}\n\nfinal_feedback: {final_feedback}\n\ncomments: {comments}\n\ncontact: {contact}", fail_silently=False, connection=None, html_message=None)

    except Exception as e:
        # print(e)
        response_data['status'] = "ERROR"
        mail_admins(f"Error at {get_current_function_name()}", f"session: {session}\n\nfinal_id: {final_id}\n\nfinal_feedback: {final_feedback}\n\ncomments: {comments}\n\ncontact: {contact}\n\nError: {str(e)}\n\n{str(request.POST)}", fail_silently=False, connection=None, html_message=None)

    return JsonResponse(response_data)

def ajax_crossover(request):
    response_data = {}

    try:
        session = request.POST.get('session')
        iteration = request.POST.get('iteration')

        parent1_id = request.POST.get('parent1_id')
        parent1 = request.POST.get('parent1')
        parent1_image = request.POST.get('parent1_image')
        parent1_json = json.loads(parent1)

        parent2_id = request.POST.get('parent2_id')
        parent2 = request.POST.get('parent2')
        parent2_image = request.POST.get('parent2_image')
        parent2_json = json.loads(parent2)

        user_input = request.POST.get('user_input')

        avoid_values = request.POST.get('avoid_values')
        avoid_values_json = json.loads(avoid_values)

        parent1_feedback = request.POST.get('parent1_feedback')
        parent1_positives = json.loads(request.POST.get('parent1_positives'))
        parent1_negatives = json.loads(request.POST.get('parent1_negatives'))
        parent1_positive_list = json.loads(request.POST.get('parent1_positive_keys'))
        parent1_negative_list = json.loads(request.POST.get('parent1_negative_keys'))

        parent2_feedback = request.POST.get('parent2_feedback')
        parent2_positives = json.loads(request.POST.get('parent2_positives'))
        parent2_negatives = json.loads(request.POST.get('parent2_negatives'))
        parent2_positive_list = json.loads(request.POST.get('parent2_positive_keys'))
        parent2_negative_list = json.loads(request.POST.get('parent2_negative_keys'))

        current_iteration_results = request.POST.get('current_iteration_results')

        UserSelectionFeedback.objects.create(
            session=session,
            iteration=iteration,
            parent1_id=parent1_id,
            parent1_json=parent1,
            parent1_image=parent1_image,
            parent1_feedback=parent1_feedback,
            parent2_id=parent2_id,
            parent2_json=parent2,
            parent2_image=parent2_image,
            parent2_feedback=parent2_feedback,
            current_iteration_results=current_iteration_results,
        )

        prompt = get_prompt_for_crossover(user_input, parent1_json, parent2_json)

        if fakecrossoverllm:
            completion, result, start_time, end_time, elapsed_time = run_fake_crossover_llm(prompt)
        else:
            completion, result, start_time, end_time, elapsed_time = run_llm(prompt)

        Crossover.objects.create(
            session=session,
            iteration=iteration,
            parent1_id=parent1_id,
            parent1=parent1,
            parent1_image=parent1_image,
            parent2_id=parent2_id,
            parent2=parent2,
            parent2_image=parent2_image,
            prompt=prompt,
            response=completion,
            result=result,
            start_time=start_time,
            end_time=end_time,
            elapsed_time=elapsed_time,
        )

        # print(completion)
        # print(result)

        result_json = json.loads(result)

        children_list = []
        result_dalle_prompt_list = []

        attributes_to_mutate = [[],[],[],[]]

        # turn result into 4 children
        for i in range(NUM_CHILDREN):
            # print(f"child {i}")
            child = {}
            # mutated = False
            for key in keyword_examples:
                random_choice_list = [parent1_json[key], parent2_json[key], result_json[key]] # include crossover result and one of each parent
                if key in parent1_positive_list:
                    random_choice_list += [parent1_json[key], parent1_json[key]] # include two more
                if key in parent2_positive_list:
                    random_choice_list += [parent2_json[key], parent2_json[key]] # include two more
                # print(f"random choice list: {random_choice_list}")
                child[key] = random.choice(random_choice_list)

                # to add, if this key value is in the bad list of either parent 1 or parent 2: if the value is the bad one, add it to the mutate list
                if key in parent1_negative_list or key in parent2_negative_list:
                    # print(f"key not liked: {key}")
                    # print(f"Child: {child}")

                    unwanted_values = []
                    if key in parent1_negatives:
                        unwanted_values.append(parent1_negatives[key])
                    if key in parent2_negatives:
                        unwanted_values.append(parent2_negatives[key])
                    # if child[key] in unwanted_values:
                    if is_unwanted(child[key], unwanted_values):
                        # print(f"value not liked {child[key]}")
                        attributes_to_mutate[i].append(key)
                        # mutated = True

            children_list.append(child)

            # if not mutated:
            if not fakecrossoverllm:
                attribute_to_randomise = random.choice(keyword_examples)
                attributes_to_mutate[i].append(attribute_to_randomise)

        Children.objects.create(
            session=session,
            iteration=iteration,
            children_after_crossover=json.dumps(children_list),
        )

        if fakecrossoverllm:
            attributes_to_mutate = [["architectural style"], ["colors"], ["site"], ["colors"]]

        # print(attributes_to_mutate)

        flattened_attributes_to_mutate = [item for sublist in attributes_to_mutate for item in sublist]

        prompt = get_prompt_for_mutation(flattened_attributes_to_mutate, avoid_values_json)

        # print(prompt)

        if fakemutationllm:
            completion, result, start_time, end_time, elapsed_time = run_fake_mutation_llm(prompt)
        else:
            completion, result, start_time, end_time, elapsed_time = run_llm(prompt)

        Mutation.objects.create(
            session=session,
            iteration=iteration,
            attributes=json.dumps(attributes_to_mutate),
            avoid_values=avoid_values,
            prompt=prompt,
            response=completion,
            result=result,
            start_time=start_time,
            end_time=end_time,
            elapsed_time=elapsed_time,
        )

        # print(completion)
        # print(result)

        mutation_result_json = json.loads(result)

        # Extract values for the key in each dictionary
        mutation_values_list = [list(attribute.values())[0] for attribute in mutation_result_json]

        # print("CHILDREN BEFORE")
        # print(children_list)

        for i in range(NUM_CHILDREN):
            # update new values
            for attribute in attributes_to_mutate[i]:
                # print(f"attribute to mutate {attribute}")
                # print(f"mutation values list {mutation_values_list}")
                children_list[i][attribute] = mutation_values_list.pop(0)
                # print(f"value of children {children_list[i][attribute]}")

        # print("CHILDREN AFTER")
        # print(children_list)

        Children.objects.create(
            session=session,
            iteration=iteration,
            children_after_mutation=json.dumps(children_list),
        )

        response_data['status'] = "OK"
        response_data['children_list'] = children_list
    except Exception as e:
        # print(e)
        response_data['status'] = "ERROR"
        mail_admins(f"Error at {get_current_function_name()}", f"parent1: {parent1}\n\nparent2: {parent2}\n\nError: {str(e)}", fail_silently=False, connection=None, html_message=None)

    return JsonResponse(response_data)


def get_current_function_name():
    return inspect.currentframe().f_back.f_code.co_name

def run_llm(prompt, temperature=0.9):
    messages = [
    {'role': 'user', 'content': prompt}
    ]
        
    start_time = timezone.now() # record the start time

    completion = client.chat.completions.create(
        model=CHATGPT_MODEL,
        messages=messages,
        temperature=temperature,
    )

    end_time = timezone.now() # record the end time

    result = completion.choices[0].message.content

    result = extract_json(result) # clean up results

    elapsed_time = (end_time - start_time).total_seconds()
    return completion, result, start_time, end_time, elapsed_time


def get_prompt_for_mutation(attributes_to_mutate, avoid_values):
    attributes_string = ""
    return_answer_string = "["
    for attribute in attributes_to_mutate:
        attributes_string += '"' + attribute + '" must be different from ' + str(avoid_values[attribute]) + '\n'
        return_answer_string += '\n{"' + attribute + '": <your answer>}",'
    return_answer_string = return_answer_string[:-1] + "\n]" # remove final comma and add ]

    prompt = f"""
    Suggest a novel value for each attribute below. Each value is a string.
    ###
    {attributes_string}
    ###

    Return your answers in JSON.
    {return_answer_string}
    """
    return prompt



def get_prompt_for_crossover(user_input, parent1, parent2):
    prompt = f"""
    Create JSON from the text below. For each attribute, suggest a new value that combines ideas from both. Each value is a string.
    ###
    {user_input}

    "architectural style"
    1. {parent1['architectural style']}
    2. {parent2['architectural style']}

    "site"
    1. {parent1['site']}
    2. {parent2['site']}

    "colors"
    1. {parent1['colors']}
    2. {parent2['colors']}

    "lighting"
    1. {parent1['lighting']}
    2. {parent2['lighting']}

    "shape/form"
    1. {parent1['shape/form']}
    2. {parent2['shape/form']}

    "materials"
    1. {parent1['materials']}
    2. {parent2['materials']}
    ###

    Return your answers in JSON.
    {{
    "architectural style": <your answer>,
    "site": <your answer>,
    "colors": <your answer>,
    "lighting": <your answer>,
    "shape/form": <your answer>,
    "materials":<your answer>
    }}
    """
    return prompt


# def get_prompt_to_convert_user_input_into_json(user_input):
#     prompt = f"""
#     Create JSON from the text.
#     ###
#     {user_input}
#     ###
#     "architectural style" examples can be and are not limited to modern, gothic, vernacular, victorian, tudor, industrial, georgian, bauhaus, baroque, greek revival, american craftsman, colonial, futurist, sustainable, mid-century modern, deconstructivism, organic, brutalist, minimalist, traditional, ornate, religious, art deco, arts and craft.

#     "site" examples can be and are not limited to rainforest, desert, cityscape, countryside, rolling hills, mountains, snow, beachside, jungle, swamp, grasslands, underwater, riverside, waterfall, caves, lake, underground.

#     "color" is the use of color in the exterior design, influencing aesthetics, mood, and spatial perception. Examples can be and are not limited to chrome, mint green, black and white, soft pink, sky blue, neon shades, muted tones, maple red, rich color, mahogany.
    
#     "lighting" examples can be and are not limited to intense backlight, soft lighting, soft moon light, crepuscular ray, volumetric lighting, front lighting, hard lighting, rainbow halo, glow in the dark, natural daylight, lit from within, street lights, uplighting, spring, autumn.

#     "form" is the overall shape and structure of a building, encompassing elements such as massing, proportions, and visual composition. Examples can be and are not limited to curvilinear, geodesic dome, cylindrical.

#     "materials" are substances used in construction, influencing aesthetics, durability, and environmental impact. Examples can be and are not limited to wood, glass, stone, concrete, brick, steel. 

#     All attributes must be filled.
#     Return your answers in JSON.
#     [4 x {{
#     "architectural style": <your answer>,
#     "site": <your answer>,
#     "color": <your answer>,
#     "lighting": <your answer>,
#     "form": <your answer>,
#     "materials": <your answer>
#     }}]
#     """
#     return prompt


def get_prompt_to_convert_user_input_into_json(user_input):
    prompt = f"""
    Create JSON by extracting appropriate attribute values for an architectural building from the text.
    ###
    {user_input}
    ###
    Find values for the following attributes:
    "architectural style"
    "site"
    "colors"
    "lighting"
    "shape/form"
    "materials"

    All attributes must be filled. If values are not specified, create appropriate values randomly. Each value is a string.
    
    Return your answers in JSON.
    [4 x {{
    "architectural style": <your answer>,
    "site": <your answer>,
    "colors": <your answer>,
    "lighting": <your answer>,
    "shape/form": <your answer>,
    "materials": <your answer>
    }}]
    """
    return prompt



def run_fake_process_user_input_llm(prompt):
    start_time = timezone.now()
    time.sleep(fakellm_delay)
    end_time = timezone.now()

    fake_results_json = [
    {
        "architectural style": "organic",
        "site": "beachside",
        "colors": "natural",
        "lighting": "natural daylight",
        "shape/form": "seashell",
        "materials": "solar panels"
    },
    {
        "architectural style": "modern",
        "site": "cityscape",
        "colors": "neutral",
        "lighting": "intense backlight",
        "shape/form": "sleek",
        "materials": "glass, steel"
    },
    {
        "architectural style": "vernacular",
        "site": "countryside",
        "colors": "earthy",
        "lighting": "soft moon light",
        "shape/form": "rustic",
        "materials": "wood, stone"
    },
    {
        "architectural style": "futurist",
        "site": "underwater",
        "colors": "bright",
        "lighting": "volumetric lighting",
        "shape/form": "sleek and curved",
        "materials": "glass, acrylic"
    }]
    fake_results_string = json.dumps(fake_results_json)

    completion = "fake"
    elapsed_time = (end_time - start_time).total_seconds()

    return completion, fake_results_string, start_time, end_time, elapsed_time


def run_fake_crossover_llm(prompt):
    start_time = timezone.now()
    time.sleep(fakellm_delay)
    end_time = timezone.now()

    fake_results_json = {
        "architectural style": "victorian-baroque",
        "site": "mountain river",
        "colors": "soft pink-dark hues",
        "lighting": "soft moon halo",
        "shape/form": "sleek and curved",
        "materials": "glass, acrylic"
    }
    fake_results_string = json.dumps(fake_results_json)

    completion = "fake"
    elapsed_time = (end_time - start_time).total_seconds()

    return completion, fake_results_string, start_time, end_time, elapsed_time


def run_fake_mutation_llm(prompt):
    start_time = timezone.now()
    time.sleep(fakellm_delay)
    end_time = timezone.now()
    fake_results_json = [{"architectural style": "modern"}, {'colors': 'black'}, {"site": "ocean"}, {"colors": "red"}]
    fake_results_string = json.dumps(fake_results_json)

    completion = "fake"
    elapsed_time = (end_time - start_time).total_seconds()

    return completion, fake_results_string, start_time, end_time, elapsed_time


def run_fake_image_prompt_llm(prompt):
    start_time = timezone.now()
    time.sleep(fakellm_delay)
    end_time = timezone.now()
    # fake_results_json = [{"architectural style": "modern"}, {"site": "ocean"}, {"color": "red"}]
    fake_results_string = "This is a fake image prompt"

    completion = "fake"
    elapsed_time = (end_time - start_time).total_seconds()

    return completion, fake_results_string, start_time, end_time, elapsed_time


def fake_generate_image(prompt):
    start_time = timezone.now()
    time.sleep(fakellm_delay)
    end_time = timezone.now()

    elapsed_time = (end_time - start_time).total_seconds()
    return "fake", "https://images.pexels.com/photos/3172740/pexels-photo-3172740.jpeg", "This is a fake revised prompt", start_time, end_time, elapsed_time
    # return "fake", "http://127.0.0.1:8000/media/images/609b5074-ea9a-40b7-957b-bc747d26c1b6.png", "This is a fake revised prompt", start_time, end_time, elapsed_time


def generate_image(prompt):
    response = ''
    
    try:
            
        start_time = timezone.now() # record the start time
        
        if DALLE_MODEL == "dall-e-2": 
            response = client.images.generate(
                model=DALLE_MODEL,
                prompt=prompt,
                size="256x256", #256x256 , 512x512 , or 1024x1024
                n=1,
            )
        else:
            response = client.images.generate(
                model=DALLE_MODEL,
                prompt=prompt,
                n=1,
            )
        end_time = timezone.now() # record the end time

        # print(response)
        image_url = response.data[0].url
        # print(image_url)
        
        revised_prompt = response.data[0].revised_prompt

        elapsed_time = (end_time - start_time).total_seconds()

        return response, image_url, revised_prompt, start_time, end_time, elapsed_time

    except Exception as e:
        # print(e)
        print(response)
        mail_admins(f"Error at {get_current_function_name()}", f"Prompt: {prompt}\n\nResponse: {response}\n\nError: {str(e)}", fail_silently=False, connection=None, html_message=None)


def convert_attributes_to_dalle_prompt(user_input, attributes):
    prompt = f"""
    You are an architect. Your text below describes an image suitable for an architecture magazine.
    ###
    {user_input}
    {attributes}
    ###
    """
    return prompt


# def ajax_mail_admin(request):
#     location = request.POST.get('location')
#     error = request.POST.get('error')
#     response = request.POST.get('response')
#     mail_admins(f"Frontend error at {location}", f"Error: {error}\n\nResponse: {response}", fail_silently=False, connection=None, html_message=None)



def ajax_get_image(request):

    response_data = {}

    try:
        session = request.POST.get('session')
        iteration = request.POST.get('iteration')
        instance = request.POST.get('instance')
        user_input = request.POST.get('user_input')
        attributes = request.POST.get('attributes')

        prompt = convert_attributes_to_dalle_prompt(user_input, attributes)

        if fakeimagegen:
            dalle_response, dalle_image_url, revised_prompt, start_time, end_time, elapsed_time = fake_generate_image(prompt)
        else:
            dalle_response, dalle_image_url, revised_prompt, start_time, end_time, elapsed_time = generate_image(prompt)

        response = requests.get(dalle_image_url)
        if response.status_code == 200:
            parsed_url = urlparse(dalle_image_url) # get the url (without url parameters)

            base, extension = os.path.splitext(parsed_url.path) # get the file extension

            image_name = str(uuid.uuid4()) + extension # generate unique name
            
            # Create a ContentFile from the binary image data
            content_file = ContentFile(response.content, name=image_name)

            if not fakeimagegen:
                image_model = Image(session=session, iteration=iteration, instance=instance, response=dalle_response, prompt=prompt, attributes=attributes, revised_prompt=revised_prompt, start_time=start_time, end_time=end_time, elapsed_time=elapsed_time)
                image_model.image.save(image_name, content_file)
                image_model.save()
                response_data['result'] = image_model.image.url
            else:
                response_data['result'] = dalle_image_url

            response_data['status'] = "OK"
            response_data['prompt'] = prompt
            response_data['revised_prompt'] = revised_prompt

        else:
            response_data['status'] = "ERROR"
            mail_admins(f"Error at {get_current_function_name()}", f"Session: {session}\n\nIteration: {iteration}\n\nInstance: {instance}\n\nUser input: {user_input}\n\nAttributes: {attributes}\n\nPrompt: {prompt}\n\nCan't get image: {dalle_image_url}\n\nError: {str(response.status_code)}", fail_silently=False, connection=None, html_message=None)

    except Exception as e:
        response_data['status'] = "ERROR"
        mail_admins(f"Error at {get_current_function_name()}", f"Session: {session}\n\nIteration: {iteration}\n\nInstance: {instance}\n\nUser input: {user_input}\n\nAttributes: {attributes}\n\nPrompt: {prompt}\n\nError: {str(e)}", fail_silently=False, connection=None, html_message=None)

    return JsonResponse(response_data)


def ajax_process_user_input(request):
    response_data = {}

    try:
        user_input = request.POST.get('user_input')
        iteration = request.POST.get('iteration')

        session = uuid.uuid4()

        # save this in case prompt breaks
        UserInputInitial.objects.create(
            session=session,
            iteration=iteration,
            user_input=user_input,
        )

        prompt = get_prompt_to_convert_user_input_into_json(user_input)

        # print(prompt)

        if fakeuserinputllm:
            completion, result, start_time, end_time, elapsed_time = run_fake_process_user_input_llm(prompt)
        else:
            completion, result, start_time, end_time, elapsed_time = run_llm(prompt)

        UserInput.objects.create(
            session=session,
            iteration=iteration,
            user_input=user_input,
            prompt=prompt,
            response=completion,
            result=result,
            start_time=start_time,
            end_time=end_time,
            elapsed_time=elapsed_time,
            version=1,
        )

        response_data['status'] = "OK"
        response_data['result'] = json.loads(result)
        response_data['session'] = session
    except Exception as e:
        response_data['status'] = "ERROR"
        mail_admins(f"Error at {get_current_function_name()}", f"User input: {user_input}\n\nError: {str(e)}", fail_silently=False, connection=None, html_message=None)

    return JsonResponse(response_data)

