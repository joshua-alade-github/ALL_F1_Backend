from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import json
from django.core.cache import cache

@api_view()
def getF1DriverStandings(request, year_slug):
    year = year_slug
    cache_key = f"DriverStandings_{year}"
    data = cache.get(cache_key, None)
    if not data:
        url = f"http://ergast.com/api/f1/{year}/driverStandings.json"
        response = requests.get(url)
        responseData = json.loads(response.text)
        data = responseData.get("MRData").get("StandingsTable").get("StandingsLists")[0].get("DriverStandings")
        cache.set(cache_key, data, 3600)

    return Response(data)

@api_view()
def getF1ConstructorStandings(request, year_slug):
    year = year_slug
    cache_key = f"ConstructorStandings_{year}"
    data = cache.get(cache_key, None)
    if not data:
        url = f"http://ergast.com/api/f1/{year}/constructorStandings.json"
        response = requests.get(url)
        responseData = json.loads(response.text)
        data = responseData.get("MRData").get("StandingsTable").get("StandingsLists")[0].get("ConstructorStandings")
        cache.set(cache_key, data, 3600)

    return Response(data)

@api_view()
def getF1Drivers(request, year_slug):
    year = year_slug
    cache_key = f"Drivers_{year}"
    data = cache.get(cache_key, None)
    if not data:
        url = f"http://ergast.com/api/f1/{year}/drivers.json"
        response = requests.get(url)
        responseData = json.loads(response.text)
        data = responseData.get("MRData").get("DriverTable").get("Drivers")
        cache.set(cache_key, data, 3600)

    return Response(data)

@api_view()
def getF1Constructors(request, year_slug):
    year = year_slug
    cache_key = f"Constructors_{year}"
    data = cache.get(cache_key, None)
    if not data:
        url = f"http://ergast.com/api/f1/{year}/constructors.json"
        response = requests.get(url)
        responseData = json.loads(response.text)
        data = responseData.get("MRData").get("ConstructorTable").get("Constructors")
        cache.set(cache_key, data, 3600)

    return Response(data)

@api_view()
def getF1Circuits(request, year_slug):
    year = year_slug
    cache_key = f"Circuits_{year}"
    data = cache.get(cache_key, None)
    if not data:
        url = f"http://ergast.com/api/f1/{year}/circuits.json"
        response = requests.get(url)
        responseData = json.loads(response.text)
        data = responseData.get("MRData").get("CircuitTable").get("Circuits")
        cache.set(cache_key, data, 3600)

    return Response(data)

@api_view()
def getF1Seasons(request):
    cache_key = f"Seasons"
    data = cache.get(cache_key, None)
    if not data:
        url = "http://ergast.com/api/f1/seasons.json?limit=10000"
        response = requests.get(url)
        responseData = json.loads(response.text)
        data = responseData.get("MRData").get("SeasonTable").get("Seasons")
        cache.set(cache_key, data, 3600)

    return Response(data)

@api_view()
def getF1Results(request, year_slug):
    year = year_slug
    cache_key = f"Results_{year}"
    data = cache.get(cache_key, None)
    if not data:
        url = f"http://ergast.com/api/f1/{year}/results/1.json"
        response = requests.get(url)
        responseData = json.loads(response.text)
        data = responseData.get("MRData").get("RaceTable").get("Races")
        cache.set(cache_key, data, 3600)

    return Response(data)

@api_view()
def getF1ResultsRound(request, year_slug, round_slug):
    year = year_slug
    raceRound = round_slug
    cache_key = f"ResultsRound_{year}_{raceRound}"
    data = cache.get(cache_key, None)
    if not data:
        url = f"http://ergast.com/api/f1/{year}/{raceRound}/results.json"
        response = requests.get(url)
        responseData = json.loads(response.text)
        data = responseData.get("MRData").get("RaceTable").get("Races")[0]
        cache.set(cache_key, data, 3600)

    return Response(data)

@api_view()
def getF1QualifyingResults(request, year_slug, round_slug):
    year = year_slug
    raceRound = round_slug
    cache_key = f"Qualifying_{year}_{raceRound}"
    data = cache.get(cache_key, None)
    if not data:
        url = f"http://ergast.com/api/f1/{year}/{raceRound}/qualifying.json"
        response = requests.get(url)
        responseData = json.loads(response.text)
        data = responseData.get("MRData").get("RaceTable").get("Races")[0]
        cache.set(cache_key, data, 3600)

    return Response(data)

@api_view()
def getF1Schedule(request, year_slug):
    year = year_slug
    cache_key = f"Schedule_{year}"
    data = cache.get(cache_key, None)
    if not data:
        url = f"http://ergast.com/api/f1/{year}.json"
        response = requests.get(url)
        responseData = json.loads(response.text)
        data = responseData.get("MRData").get("RaceTable").get("Races")
        cache.set(cache_key, data, 3600)

    return Response(data)