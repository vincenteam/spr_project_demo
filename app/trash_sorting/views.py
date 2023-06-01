import json
from collections import OrderedDict
import requests

# Create your views here.
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from .models import SortSystem, Bin, Content, ContentType, Address

def current_datetime(request):
    return HttpResponse("lorem ipsum")

def load_bins_data(bins_ids):
    bins_data = {}
    for b in [Bin.objects.get(id=id) for id in bins_ids]:
        bin_content = b.contents.all()
        bins_data[b] = {}
        for content in bin_content:
            if content.type not in bins_data[b].keys():
                bins_data[b][content.type] = [content]
            else:
                bins_data[b][content.type].append(content)

    return bins_data


def get_address_from_coords(lat:str, lon:str):
    url = "https://nominatim.openstreetmap.org/reverse?lat={}&lon={}&zoom=18&addressdetails=1&accept-language=en&format=json".format(lat, lon)
    res = requests.get(url)
    print(res.text)
    reverse_geocoded = json.loads(res.text, object_pairs_hook=OrderedDict)

    return reverse_geocoded["address"] if "address" in reverse_geocoded else None

def get_sort_system(address:OrderedDict):
    systems_addresses = {}

    for sys_address in Address.objects.all():
        system_id = sys_address.parent_system.id
        if system_id in systems_addresses:
            systems_addresses[system_id].append(json.loads(sys_address.address, object_pairs_hook=OrderedDict))
        else:
            systems_addresses[system_id] = [json.loads(sys_address.address, object_pairs_hook=OrderedDict)]

    #print("sys addrs ", systems_addresses)
    #print("req addr ", address)
    longest_match:(int, int) = None
    for sort_system_item in systems_addresses.items():
        for sys_address in sort_system_item[1]:
            match = True
            for field_item in reversed(sys_address.items()):
                if not field_item[0] in address or not address[field_item[0]] == field_item[1]:
                    match = False
                    break
            if match:
                match_len = len(sys_address)
                if longest_match is None or match_len > longest_match[1]:
                    longest_match = (sort_system_item[0], match_len)

    #print(longest_match)

    return longest_match[0] if longest_match is not None else None


@csrf_exempt
def test(request):
    if "lat" in request.POST and "lon" in request.POST:
        print(get_address_from_coords(request.POST["lat"], request.POST["lon"]))
    return HttpResponse("res")

@csrf_exempt
def search(request):

    any_name = "any"
    choice_other = "other"
    search_session_variable = ["user_choices", "types_done_ids", "bins_ids"]
    new_search_session_var = "new_search"
    location_session_var = "location"
    lat_session_var = "lat"
    lon_session_var = "lon"

    new_search = False

    res = "res: "


    if new_search_session_var in request.POST:
        new_search = True
        for var in search_session_variable:
            request.session.pop(var, None)

        # replace with for loop in sessions_var
        request.session["user_choices"] = []
        request.session["types_done_ids"] = []


    #get location
    if lat_session_var in request.POST and lon_session_var in request.POST:
        lat = request.POST[lat_session_var]
        lon = request.POST[lon_session_var]
        request_addr = get_address_from_coords(lat, lon)

        if request_addr is None:
            res = "location lat:{}°, lon {}° does not exist in the database".format(lat, lon)
            return HttpResponse(res)

        sort_system_id = get_sort_system(request_addr)
        if sort_system_id is None:
            res = "location lat:{}°, lon {}° does not exist in the database".format(lat, lon)
            return HttpResponse(res)
        else:
            res += " {} \n".format(SortSystem.objects.filter(id=sort_system_id)[0].name)
            request.session[location_session_var] = sort_system_id
            print("new location")
    elif not location_session_var in request.session:
        res = "location is needed to make a research"
        return HttpResponse(res)


    #get bins ids
    sort_system = request.session[location_session_var]
    if not "bins_ids" in request.session:
        print("load bins from base")
        request.session["bins_ids"] = [b.id for b in  Bin.objects.filter(parent_system=sort_system)]
    bins_ids = request.session["bins_ids"]

    #get last user choice
    try:
        choice = request.POST["choice"]
    except KeyError:
        print("no user choice")
        choice = None
    request.session["user_choices"].append(choice)

    bins_data = load_bins_data(bins_ids)


    # modify bin list according to choice
    if choice and not new_search:
        print(bins_data.keys())

        for b_items in bins_data.items():
            content_found = False
            choice_type_id = request.session["types_done_ids"][-1]
            if choice_type_id in [t.id for t in b_items[1].keys()]:
                choice_type = next(t for t in b_items[1].keys() if t.id == choice_type_id)
                print("type in")
                names = [i.name for i in b_items[1][choice_type]]
                print(names, choice)
                if choice == choice_other:
                    if any_name in names:
                        content_found = True
                    else:
                        content_found = True
                        for ch in request.session["choices"]:
                            if ch in names:
                                content_found = False
                                break
                elif choice in names or any_name in names:
                    content_found = True
            else:
                if choice == choice_other:
                    content_found = True
            if not content_found:
                print("remove ", b_items[0].name, b_items[0].id)
                bins_ids.remove(b_items[0].id)

        request.session["bins_ids"] = bins_ids
        bins_data = load_bins_data(bins_ids)



    # create next question
    print(bins_data)
    types = {}
    for b in bins_data.values():
        for t in b.keys():
            if t.id not in request.session["types_done_ids"] and any_name not in [c.name for c in b[t]]:
                if t not in types.keys():
                    types[t] = len(b[t])
                else:
                    types[t] += len(b[t])

    print(types)

    def bin_priority(b):
        priority = 0
        for c_item in bins_data[b].items():
            if any_name in [c.name for c in c_item[1]]:
                priority += 1
        return priority

    # check for end condition
    if len(types) == 0:
        print("bin found")

        nb_fitting_bins = len(bins_data)
        if nb_fitting_bins == 0:
            print("no bin fit")
            bin_name = "no bin"
        elif nb_fitting_bins == 1:
            print("easy")
            bin_name = str(next(iter(bins_data)))
        else:
            print("multiple choices")
            bins_keys = list(bins_data.keys())
            list.sort(bins_keys, key=bin_priority)
            print(bins_keys)
            bin_name = str(bins_keys[0])
        res = "bin found: " + bin_name
        return HttpResponse(res)

    most_common_type = max(types, key=types.get)
    request.session["types_done_ids"].append(most_common_type.id)
    choices = []
    for b in bins_data.values():
        for item in b.items():
            if item[0].name == most_common_type.name:
                choices += item[1]
    choices = list(set(choices))

    print(most_common_type)
    print(choices)
    request.session["choices"] = [c.name for c in choices if c.name != any_name]
    request.session["choices"].append(choice_other)
    print(request.session["choices"])
    res += str(request.session["choices"])
    return HttpResponse(res)