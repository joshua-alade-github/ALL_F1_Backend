from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import json

@api_view()
def getF1DriverStandings(request, year_slug):
    year = year_slug
    url = f"http://ergast.com/api/f1/{year}/driverStandings.json"
    response = requests.get(url)
    responseData = json.loads(response.text)
    data = responseData.get("MRData").get("StandingsTable").get("StandingsLists")[0].get("DriverStandings")

    return Response(data)

@api_view()
def getF1ConstructorStandings(request, year_slug):
    year = year_slug
    url = f"http://ergast.com/api/f1/{year}/constructorStandings.json"
    response = requests.get(url)
    responseData = json.loads(response.text)
    data = responseData.get("MRData").get("StandingsTable").get("StandingsLists")[0].get("ConstructorStandings")

    return Response(data)

@api_view()
def getF1Drivers(request, year_slug):
    year = year_slug
    url = f"http://ergast.com/api/f1/{year}/drivers.json"
    response = requests.get(url)
    responseData = json.loads(response.text)
    data = responseData.get("MRData").get("DriverTable").get("Drivers")

    return Response(data)

@api_view()
def getF1Constructors(request, year_slug):
    year = year_slug
    url = f"http://ergast.com/api/f1/{year}/constructors.json"
    response = requests.get(url)
    responseData = json.loads(response.text)
    data = responseData.get("MRData").get("ConstructorTable").get("Constructors")

    return Response(data)

@api_view()
def getF1Circuits(request, year_slug):
    year = year_slug
    url = f"http://ergast.com/api/f1/{year}/circuits.json"
    response = requests.get(url)
    responseData = json.loads(response.text)
    data = responseData.get("MRData").get("CircuitTable").get("Circuits")

    return Response(data)

@api_view()
def getF1Seasons(request):
    url = "http://ergast.com/api/f1/seasons.json?limit=10000"
    response = requests.get(url)
    responseData = json.loads(response.text)
    data = responseData.get("MRData").get("SeasonTable").get("Seasons")

    return Response(data)

@api_view()
def getF1Results(request, year_slug):
    year = year_slug
    url = f"http://ergast.com/api/f1/{year}/results/1.json"
    response = requests.get(url)
    responseData = json.loads(response.text)
    data = responseData.get("MRData").get("RaceTable").get("Races")

    return Response(data)

@api_view()
def getF1ResultsRound(request, year_slug, round_slug):
    year = year_slug
    raceRound = round_slug
    url = f"http://ergast.com/api/f1/{year}/{raceRound}/results.json"
    response = requests.get(url)
    responseData = json.loads(response.text)
    data = responseData.get("MRData").get("RaceTable").get("Races")[0]

    return Response(data)

@api_view()
def getF1QualifyingResults(request, year_slug, round_slug):
    year = year_slug
    raceRound = round_slug
    url = f"http://ergast.com/api/f1/{year}/{raceRound}/qualifying.json"
    response = requests.get(url)
    responseData = json.loads(response.text)
    data = responseData.get("MRData").get("RaceTable").get("Races")[0]

    return Response(data)

@api_view()
def getF1Schedule(request, year_slug):
    year = year_slug
    url = f"http://ergast.com/api/f1/{year}.json"
    response = requests.get(url)
    responseData = json.loads(response.text)
    data = responseData.get("MRData").get("RaceTable").get("Races")

    return Response(data)