import time
import asyncio
from http_client import download_http10, download_http11, download_http2 
import matplotlib.pyplot as plt

# Mesurer le temps d'exécution d'une fonction HTTP
def measure_http_performance(url, protocol_function):
    start_time = time.perf_counter()
    protocol_function(url)  # Appeler la fonction passée en paramètre
    end_time = time.perf_counter()
    return end_time - start_time

# Mesurer une fonction asynchrone (HTTP/2)
async def measure_http_performance_async(url, protocol_function):
    start_time = time.perf_counter()
    await protocol_function(url)  # Appeler la fonction asynchrone
    end_time = time.perf_counter()
    return end_time - start_time

# Générer un graphique des résultats
def plot_performance(results):
    protocols = list(results.keys())
    times = list(results.values())

    plt.bar(protocols, times, color=['blue', 'green','red'])
    plt.xlabel("Protocole HTTP")
    plt.ylabel("Temps (secondes)")
    plt.title("Comparaison des performances HTTP")
    plt.show()

if __name__ == "__main__":
    #url = "http://www.google.com"  # URL à tester
    
    url = input("Entrez un url svp ! ")


    # Mesurer les performances pour HTTP/1.0
    print("Test HTTP/1.0...")
    time_http10 = measure_http_performance(url, download_http10)
    
    # Mesurer les performances pour HTTP/1.1
    print("Test HTTP/1.1...")
    time_http11 = measure_http_performance(url, download_http11)

    # Mesurer les performances pour HTTP/2
    print("Test HTTP/2...")
    time_http2 = asyncio.run(measure_http_performance_async(url, download_http2))

    # Afficher les résultats
    results = {
        "HTTP/1.0": time_http10,
        "HTTP/1.1": time_http11,
        "HTTP/2": time_http2
    }

    print("Résultats des performances :")
    for protocol, time_taken in results.items():
        print(f"{protocol} : {time_taken:.2f} secondes")

    # Générer le graphique
    plot_performance(results)
