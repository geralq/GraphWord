import string
import nltk
from nltk.corpus import stopwords
import os
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

# Descargar los recursos necesarios de NLTK (solo la primera vez)
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)


def obtener_vocabulario_con_cuentas(filename, eliminar_stopwords=False):
    """
    Extrae el vocabulario de palabras de tres letras de un archivo de texto y cuenta sus apariciones.

    Args:
        filename (str): Ruta al archivo de texto.
        eliminar_stopwords (bool): Si True, elimina las palabras comunes (stop words).

    Returns:
        dict: Diccionario donde las llaves son palabras de tres letras y los valores son sus cuentas.
    """
    # Verificar si el archivo existe
    if not os.path.isfile(filename):
        print(f"Error: El archivo '{filename}' no se encuentra.")
        print(f"Ruta absoluta: {os.path.abspath(filename)}")
        return {}

    try:
        # Leer el contenido del archivo con una codificación específica
        with open(filename, 'r', encoding='utf-8') as file:
            texto = file.read()
    except UnicodeDecodeError:
        print("Error de decodificación con 'utf-8'. Intentando con 'latin-1'.")
        try:
            with open(filename, 'r', encoding='latin-1') as file:
                texto = file.read()
        except Exception as e:
            print(f"Error al leer el archivo con 'latin-1': {e}")
            return {}
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return {}

    # Convertir texto a minúsculas
    texto = texto.lower()

    # Eliminar signos de puntuación y otros caracteres no alfabéticos
    texto = ''.join([char if char.isalpha() or char.isspace() else ' ' for char in texto])

    # Tokenizar el texto
    palabras = nltk.word_tokenize(texto)

    # Filtrar palabras de tres letras
    palabras_tres_letras = [palabra for palabra in palabras if len(palabra) == 3]

    if eliminar_stopwords:
        # Obtener la lista de stop words en inglés
        stop_words = set(stopwords.words('english'))
        # Eliminar stop words
        palabras_tres_letras = [palabra for palabra in palabras_tres_letras if palabra not in stop_words]

    # Contar las apariciones de cada palabra
    contador = Counter(palabras_tres_letras)

    return contador


def difiere_por_una_letra(palabra1, palabra2):
    """
    Verifica si dos palabras de tres letras difieren en exactamente una letra.

    Args:
        palabra1 (str): Primera palabra.
        palabra2 (str): Segunda palabra.

    Returns:
        bool: True si difieren en una letra, False de lo contrario.
    """
    diferencias = sum(1 for a, b in zip(palabra1, palabra2) if a != b)
    return diferencias == 1


def construir_grafo_con_pesos(contador_palabras):
    """
    Construye un grafo donde cada nodo es una palabra y las aristas conectan palabras que difieren en una letra.
    Los pesos de las aristas se basan en las cuentas de las palabras conectadas.

    Args:
        contador_palabras (dict): Diccionario con palabras como llaves y sus cuentas como valores.

    Returns:
        networkx.Graph: El grafo construido con pesos en las aristas.
    """
    G = nx.Graph()

    # Añadir nodos con atributo de cuenta
    for palabra, cuenta in contador_palabras.items():
        G.add_node(palabra, cuenta=cuenta)

    # Convertir las palabras a una lista para iterar con índices
    palabras = list(contador_palabras.keys())
    n = len(palabras)

    # Añadir aristas con pesos
    for i in range(n):
        for j in range(i + 1, n):
            palabra1 = palabras[i]
            palabra2 = palabras[j]
            if difiere_por_una_letra(palabra1, palabra2):
                cuenta1 = contador_palabras[palabra1]
                cuenta2 = contador_palabras[palabra2]
                peso = (cuenta1 + cuenta2) / 2
                G.add_edge(palabra1, palabra2, peso=peso)

    return G


def construir_grafo_con_pesos_optimizado(contador_palabras):
    """
    Construye un grafo optimizado donde cada nodo es una palabra y las aristas conectan palabras que difieren en una letra.
    Los pesos de las aristas se basan en las cuentas de las palabras conectadas.

    Utiliza un método optimizado para reducir la complejidad temporal.

    Args:
        contador_palabras (dict): Diccionario con palabras como llaves y sus cuentas como valores.

    Returns:
        networkx.Graph: El grafo construido con pesos en las aristas.
    """
    G = nx.Graph()

    # Añadir nodos con atributo de cuenta
    for palabra, cuenta in contador_palabras.items():
        G.add_node(palabra, cuenta=cuenta)

    # Crear un diccionario para agrupar palabras por patrones
    patrones = {}
    for palabra in contador_palabras:
        for i in range(3):
            patron = palabra[:i] + '_' + palabra[i + 1:]
            patrones.setdefault(patron, set()).add(palabra)

    # Añadir aristas basadas en patrones
    for grupo in patrones.values():
        grupo = list(grupo)
        n = len(grupo)
        for i in range(n):
            for j in range(i + 1, n):
                palabra1 = grupo[i]
                palabra2 = grupo[j]
                cuenta1 = contador_palabras[palabra1]
                cuenta2 = contador_palabras[palabra2]
                peso = (cuenta1 + cuenta2) / 2
                G.add_edge(palabra1, palabra2, peso=peso)

    return G


def visualizar_grafo_con_pesos(G):
    """
    Visualiza el grafo usando matplotlib, ajustando el grosor de las aristas según su peso.

    Args:
        G (networkx.Graph): El grafo a visualizar.
    """
    plt.figure(figsize=(15, 15))

    # Obtener los pesos de las aristas para ajustar el grosor
    pesos = [G[u][v]['peso'] for u, v in G.edges()]

    # Normalizar los pesos para el grosor de las aristas
    max_peso = max(pesos) if pesos else 1
    min_peso = min(pesos) if pesos else 1
    # Evitar división por cero
    if max_peso == min_peso:
        widths = [1 for _ in pesos]
    else:
        widths = [1 + 4 * ((peso - min_peso) / (max_peso - min_peso)) for peso in pesos]  # Grosor entre 1 y 5

    pos = nx.spring_layout(G, k=0.15, iterations=20, seed=42)  # Algoritmo de posicionamiento

    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_size=50, node_color='blue', alpha=0.7)

    # Dibujar aristas con grosor basado en el peso
    nx.draw_networkx_edges(G, pos, width=widths, alpha=0.5)

    # Opcional: Dibujar etiquetas de nodos (puede ser muy denso)
    # nx.draw_networkx_labels(G, pos, font_size=8)

    plt.title("Grafo de Palabras de Tres Letras con Pesos en las Aristas")
    plt.axis('off')
    plt.show()


def visualizar_grafo_con_pesos_mejorado(G):
    """
    Visualiza el grafo usando matplotlib, ajustando el grosor de las aristas según su peso y el tamaño de los nodos según su cuenta.

    Args:
        G (networkx.Graph): El grafo a visualizar.
    """
    plt.figure(figsize=(15, 15))

    # Obtener los pesos de las aristas para ajustar el grosor
    pesos = [G[u][v]['peso'] for u, v in G.edges()]

    # Normalizar los pesos para el grosor de las aristas
    max_peso = max(pesos) if pesos else 1
    min_peso = min(pesos) if pesos else 1
    # Evitar división por cero
    if max_peso == min_peso:
        widths = [1 for _ in pesos]
    else:
        widths = [1 + 4 * ((peso - min_peso) / (max_peso - min_peso)) for peso in pesos]  # Grosor entre 1 y 5

    pos = nx.spring_layout(G, k=0.15, iterations=20, seed=42)  # Algoritmo de posicionamiento

    # Obtener cuentas para ajustar el tamaño de los nodos
    cuentas = [G.nodes[n]['cuenta'] for n in G.nodes()]
    max_cuenta = max(cuentas) if cuentas else 1
    min_cuenta = min(cuentas) if cuentas else 1
    # Normalizar cuentas para el tamaño de los nodos
    if max_cuenta == min_cuenta:
        tamaños = [300 for _ in cuentas]
    else:
        tamaños = [300 + 700 * ((cuenta - min_cuenta) / (max_cuenta - min_cuenta)) for cuenta in
                   cuentas]  # Tamaño entre 300 y 1000

    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_size=tamaños, node_color='blue', alpha=0.7)

    # Dibujar aristas con grosor basado en el peso
    nx.draw_networkx_edges(G, pos, width=widths, alpha=0.5)

    # Opcional: Dibujar etiquetas de nodos (puede ser muy denso)
    # nx.draw_networkx_labels(G, pos, font_size=8)

    plt.title("Grafo de Palabras de Tres Letras con Pesos en las Aristas")
    plt.axis('off')
    plt.show()


def hamming_distance(palabra1, palabra2):
    """
    Calcula la distancia de Hamming entre dos palabras de igual longitud.

    Args:
        palabra1 (str): Primera palabra.
        palabra2 (str): Segunda palabra.

    Returns:
        int: Número de posiciones en las que las letras difieren.
    """
    return sum(c1 != c2 for c1, c2 in zip(palabra1, palabra2))


def calcular_camino_mas_corto(G, palabra_origen, palabra_destino, algoritmo='dijkstra'):
    """
    Calcula el camino más corto entre dos palabras en el grafo utilizando Dijkstra o A*.

    Args:
        G (networkx.Graph): El grafo donde buscar el camino.
        palabra_origen (str): Palabra de origen.
        palabra_destino (str): Palabra de destino.
        algoritmo (str): Algoritmo a usar ('dijkstra' o 'astar').

    Returns:
        list: Lista de palabras que forman el camino más corto, o None si no existe.
    """
    if palabra_origen not in G.nodes:
        print(f"Error: La palabra de origen '{palabra_origen}' no está en el grafo.")
        return None
    if palabra_destino not in G.nodes:
        print(f"Error: La palabra de destino '{palabra_destino}' no está en el grafo.")
        return None
    if algoritmo not in ['dijkstra', 'astar']:
        print("Error: El algoritmo debe ser 'dijkstra' o 'astar'.")
        return None

    try:
        if algoritmo == 'dijkstra':
            camino = nx.dijkstra_path(G, palabra_origen, palabra_destino, weight='peso')
        elif algoritmo == 'astar':
            camino = nx.astar_path(G, palabra_origen, palabra_destino, heuristic=lambda u, v: hamming_distance(u, v),
                                   weight='peso')
        return camino
    except nx.NetworkXNoPath:
        print(f"No existe un camino entre '{palabra_origen}' y '{palabra_destino}'.")
        return None
    except Exception as e:
        print(f"Error al calcular el camino: {e}")
        return None


def visualizar_camino(G, camino):
    """
    Visualiza el grafo y resalta el camino especificado.

    Args:
        G (networkx.Graph): El grafo a visualizar.
        camino (list): Lista de palabras que forman el camino a resaltar.
    """
    plt.figure(figsize=(15, 15))

    # Obtener los pesos de las aristas para ajustar el grosor
    pesos = [G[u][v]['peso'] for u, v in G.edges()]

    # Normalizar los pesos para el grosor de las aristas
    max_peso = max(pesos) if pesos else 1
    min_peso = min(pesos) if pesos else 1
    # Evitar división por cero
    if max_peso == min_peso:
        widths = [1 for _ in pesos]
    else:
        widths = [1 + 4 * ((peso - min_peso) / (max_peso - min_peso)) for peso in pesos]  # Grosor entre 1 y 5

    pos = nx.spring_layout(G, k=0.15, iterations=20, seed=42)  # Algoritmo de posicionamiento

    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_size=50, node_color='blue', alpha=0.7)

    # Dibujar aristas con grosor basado en el peso
    nx.draw_networkx_edges(G, pos, width=widths, alpha=0.3)

    # Resaltar el camino
    if camino:
        # Crear una lista de aristas en el camino
        camino_aristas = list(zip(camino, camino[1:]))
        # Dibujar las aristas del camino con mayor grosor y color rojo
        nx.draw_networkx_edges(G, pos, edgelist=camino_aristas, width=4, edge_color='red')
        # Dibujar los nodos del camino con un color diferente
        nx.draw_networkx_nodes(G, pos, nodelist=camino, node_size=100, node_color='red', alpha=0.9)

    # Opcional: Dibujar etiquetas de nodos (puede ser muy denso)
    # nx.draw_networkx_labels(G, pos, font_size=8)

    plt.title("Grafo de Palabras de Tres Letras con Camino Resaltado")
    plt.axis('off')
    plt.show()


def main():
    # Uso del script
    filename = r'C:\Users\gerar\OneDrive\Escritorio\Cuarto\TSCD\GraphWord\Datalake\pg74507.txt'

    # Opcional: Imprimir el directorio actual para verificar rutas relativas
    print(f"Directorio actual: {os.getcwd()}")

    # Obtener el contador de palabras de tres letras
    contador_palabras = obtener_vocabulario_con_cuentas(filename, eliminar_stopwords=True)

    if contador_palabras:
        print(f"\nTotal de palabras de tres letras (únicas): {len(contador_palabras)}")
        print("Algunas palabras de tres letras y sus cuentas:")
        for palabra, cuenta in list(contador_palabras.items())[:10]:
            print(f"{palabra}: {cuenta}")

        # Construir el grafo con pesos (elige una de las dos funciones)
        # G = construir_grafo_con_pesos(contador_palabras)  # Método no optimizado
        G = construir_grafo_con_pesos_optimizado(contador_palabras)  # Método optimizado
        print(f"\nTotal de nodos en el grafo: {G.number_of_nodes()}")
        print(f"Total de aristas en el grafo: {G.number_of_edges()}")

        # Opcional: Imprimir algunas aristas con sus pesos
        print("\nAlgunas aristas con sus pesos:")
        for u, v, data in list(G.edges(data=True))[:10]:
            print(f"{u} - {v}: Peso = {data['peso']}")

        # Visualizar el grafo
        # visualizar_grafo_con_pesos(G)  # Método de visualización básico
        visualizar_grafo_con_pesos_mejorado(G)  # Método de visualización mejorado

        # Solicitar al usuario las palabras de origen y destino
        while True:
            print("\n--- Cálculo del Camino Más Corto ---")
            palabra_origen = input("Ingrese la palabra de origen (o 'salir' para terminar): ").lower()
            if palabra_origen == 'salir':
                break
            palabra_destino = input("Ingrese la palabra de destino (o 'salir' para terminar): ").lower()
            if palabra_destino == 'salir':
                break
            algoritmo = input("Seleccione el algoritmo ('dijkstra' o 'astar'): ").lower()
            if algoritmo not in ['dijkstra', 'astar']:
                print("Algoritmo no válido. Por favor, elija 'dijkstra' o 'astar'.")
                continue

            # Calcular el camino más corto
            camino = calcular_camino_mas_corto(G, palabra_origen, palabra_destino, algoritmo=algoritmo)

            if camino:
                print(
                    f"\nCamino más corto entre '{palabra_origen}' y '{palabra_destino}' usando {algoritmo.capitalize()}:")
                print(" -> ".join(camino))

                # Visualizar el camino en el grafo
                visualizar_camino(G, camino)
            else:
                print("No se pudo encontrar un camino entre las palabras especificadas.")
    else:
        print("No se pudo obtener el vocabulario debido a un error anterior.")


if __name__ == "__main__":
    main()
