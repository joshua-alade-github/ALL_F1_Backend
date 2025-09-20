from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import json
from django.core.cache import cache
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

# Updated base URL to Jolpica (Ergast mirror)
ERGAST_BASE_URL = "https://api.jolpi.ca/ergast/f1"

def get_cache_timeout(year):
    """Variable cache timeout based on season year"""
    try:
        current_year = datetime.now().year
        year_int = int(year) if year else current_year
        
        if year_int < current_year:
            return 86400 * 7
        elif year_int == current_year:
            return 3600
        else:
            return 86400
    except:
        return 3600

def handle_api_error(error, data_type):
    """Consistent error handling for API calls"""
    print(f"Error fetching {data_type}: {error}")
    return Response({
        'error': True,
        'message': f'Failed to fetch {data_type} from F1 API',
        'data': [] if data_type != 'race' else {}
    }, status=500)

@api_view(['GET'])
def getF1DriverStandings(request, year_slug):
    year = year_slug
    cache_key = f"DriverStandings_{year}"
    data = cache.get(cache_key, None)
    
    if not data:
        try:
            url = f"{ERGAST_BASE_URL}/{year}/driverStandings.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            responseData = response.json()
            
            standings_lists = responseData.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
            if standings_lists:
                data = standings_lists[0].get("DriverStandings", [])
            else:
                data = []
                
            cache.set(cache_key, data, get_cache_timeout(year))
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "driver standings")
        except Exception as e:
            return handle_api_error(e, "driver standings")

    return Response({'error': False, 'data': data})

@api_view(['GET'])
def getF1ConstructorStandings(request, year_slug):
    year = year_slug
    cache_key = f"ConstructorStandings_{year}"
    data = cache.get(cache_key, None)
    
    if not data:
        try:
            url = f"{ERGAST_BASE_URL}/{year}/constructorStandings.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            responseData = response.json()
            
            standings_lists = responseData.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
            if standings_lists:
                data = standings_lists[0].get("ConstructorStandings", [])
            else:
                data = []
                
            cache.set(cache_key, data, get_cache_timeout(year))
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "constructor standings")
        except Exception as e:
            return handle_api_error(e, "constructor standings")

    return Response({'error': False, 'data': data})

@api_view(['GET'])
def getF1Drivers(request, year_slug):
    year = year_slug
    cache_key = f"Drivers_{year}"
    data = cache.get(cache_key, None)
    
    if not data:
        try:
            url = f"{ERGAST_BASE_URL}/{year}/drivers.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            responseData = response.json()
            data = responseData.get("MRData", {}).get("DriverTable", {}).get("Drivers", [])
            cache.set(cache_key, data, get_cache_timeout(year))
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "drivers")
        except Exception as e:
            return handle_api_error(e, "drivers")

    return Response({'error': False, 'data': data})

@api_view(['GET'])
def getF1Constructors(request, year_slug):
    year = year_slug
    cache_key = f"Constructors_{year}"
    data = cache.get(cache_key, None)
    
    if not data:
        try:
            url = f"{ERGAST_BASE_URL}/{year}/constructors.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            responseData = response.json()
            data = responseData.get("MRData", {}).get("ConstructorTable", {}).get("Constructors", [])
            cache.set(cache_key, data, get_cache_timeout(year))
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "constructors")
        except Exception as e:
            return handle_api_error(e, "constructors")

    return Response({'error': False, 'data': data})

@api_view(['GET'])
def getF1Circuits(request, year_slug):
    year = year_slug
    cache_key = f"Circuits_{year}"
    data = cache.get(cache_key, None)
    
    if not data:
        try:
            url = f"{ERGAST_BASE_URL}/{year}/circuits.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            responseData = response.json()
            data = responseData.get("MRData", {}).get("CircuitTable", {}).get("Circuits", [])
            cache.set(cache_key, data, get_cache_timeout(year))
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "circuits")
        except Exception as e:
            return handle_api_error(e, "circuits")

    return Response({'error': False, 'data': data})

@api_view(['GET'])
def getF1Seasons(request):
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 30))
    
    cache_key = f"AllSeasons"
    all_seasons_data = cache.get(cache_key, None)
    
    if not all_seasons_data:
        try:
            url = f"{ERGAST_BASE_URL}/seasons.json?limit=100"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            responseData = response.json()
            
            mrdata = responseData.get("MRData", {})
            all_seasons = mrdata.get("SeasonTable", {}).get("Seasons", [])
            
            all_seasons.sort(key=lambda x: int(x.get('season', 0)), reverse=True)
            
            all_seasons_data = all_seasons
            cache.set(cache_key, all_seasons_data, 86400 * 7)
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "seasons")
        except Exception as e:
            return handle_api_error(e, "seasons")
    
    total = len(all_seasons_data)
    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, total)
    
    paginated_seasons = all_seasons_data[start_index:end_index]
    
    data = {
        'seasons': paginated_seasons,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': (total + per_page - 1) // per_page
        }
    }
    
    return Response({'error': False, 'data': data})
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 30))
    offset = (page - 1) * per_page
    
    cache_key = f"Seasons_page_{page}_perpage_{per_page}"
    data = cache.get(cache_key, None)
    
    if not data:
        try:
            url = f"{ERGAST_BASE_URL}/seasons.json?limit={per_page}&offset={offset}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            responseData = response.json()
            
            mrdata = responseData.get("MRData", {})
            seasons = mrdata.get("SeasonTable", {}).get("Seasons", [])
            total = int(mrdata.get("total", 0))
            
            data = {
                'seasons': seasons,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'total_pages': (total + per_page - 1) // per_page
                }
            }
            
            cache.set(cache_key, data, 86400 * 7)
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "seasons")
        except Exception as e:
            return handle_api_error(e, "seasons")

    return Response({'error': False, 'data': data})

@api_view(['GET'])
def getF1Results(request, year_slug):
    year = year_slug
    cache_key = f"Results_{year}"
    data = cache.get(cache_key, None)
    
    if not data:
        try:
            url = f"{ERGAST_BASE_URL}/{year}/results/1.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            responseData = response.json()
            data = responseData.get("MRData", {}).get("RaceTable", {}).get("Races", [])
            cache.set(cache_key, data, get_cache_timeout(year))
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "results")
        except Exception as e:
            return handle_api_error(e, "results")

    return Response({'error': False, 'data': data})

@api_view(['GET'])
def getF1ResultsRound(request, year_slug, round_slug):
    year = year_slug
    raceRound = round_slug
    cache_key = f"ResultsRound_{year}_{raceRound}"
    data = cache.get(cache_key, None)
    
    if not data:
        try:
            url = f"{ERGAST_BASE_URL}/{year}/{raceRound}/results.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            responseData = response.json()
            races = responseData.get("MRData", {}).get("RaceTable", {}).get("Races", [])
            
            if races:
                data = races[0]
            else:
                return Response({
                    'error': True,
                    'message': 'Race not found',
                    'data': {}
                }, status=404)
                
            cache.set(cache_key, data, get_cache_timeout(year))
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return Response({
                    'error': True,
                    'message': 'Race not found',
                    'data': {}
                }, status=404)
            return handle_api_error(e, "race")
        except Exception as e:
            return handle_api_error(e, "race")

    return Response({'error': False, 'data': data})

@api_view(['GET'])
def getF1QualifyingResults(request, year_slug, round_slug):
    year = year_slug
    raceRound = round_slug
    cache_key = f"Qualifying_{year}_{raceRound}"
    data = cache.get(cache_key, None)
    
    if not data:
        try:
            url = f"{ERGAST_BASE_URL}/{year}/{raceRound}/qualifying.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            responseData = response.json()
            races = responseData.get("MRData", {}).get("RaceTable", {}).get("Races", [])
            
            if races:
                data = races[0]
            else:
                return Response({
                    'error': True,
                    'message': 'Qualifying results not found',
                    'data': {}
                }, status=404)
                
            cache.set(cache_key, data, get_cache_timeout(year))
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return Response({
                    'error': True,
                    'message': 'Qualifying results not found',
                    'data': {}
                }, status=404)
            return handle_api_error(e, "qualifying")
        except Exception as e:
            return handle_api_error(e, "qualifying")

    return Response({'error': False, 'data': data})

@api_view(['GET'])
def getF1Schedule(request, year_slug):
    year = year_slug
    cache_key = f"Schedule_{year}"
    data = cache.get(cache_key, None)
    
    if not data:
        try:
            url = f"{ERGAST_BASE_URL}/{year}.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            responseData = response.json()
            data = responseData.get("MRData", {}).get("RaceTable", {}).get("Races", [])
            cache.set(cache_key, data, get_cache_timeout(year))
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "schedule")
        except Exception as e:
            return handle_api_error(e, "schedule")

    return Response({'error': False, 'data': data})

@api_view(['POST'])
@csrf_exempt
def clearCache(request):
    try:
        cache.clear()
        return Response({
            'error': False,
            'message': 'Cache cleared successfully',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return Response({
            'error': True,
            'message': f'Failed to clear cache: {str(e)}'
        }, status=500)

@api_view(['GET'])
def healthCheck(request):
    try:
        url = f"{ERGAST_BASE_URL}/seasons.json?limit=1"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        return Response({
            'status': 'healthy',
            'api_provider': 'Jolpica',
            'cache_enabled': True,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }, status=503)