import httpx
import aioquic
import asyncio
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration
from urllib.parse import urlparse


# HTTP/10 client
def download_http10(url):
    with httpx.Client(http2=False) as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Erreur HTTP : {response.status_code}")
    
# HTTP/1.1 client
def download_http11(url):
    with httpx.Client(http2=False) as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Erreur HTTP : {response.status_code}")

# HTTP/2 client
async def download_http2(url):
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Erreur HTTP : {response.status_code}")
        
# HTTP/3 client using aioquic
async def download_http3(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme != "https":
        raise ValueError("HTTP/3 requires a secure 'https' URL")

    host = parsed_url.hostname
    port = parsed_url.port or 443

    # Configure the QUIC connection
    configuration = QuicConfiguration(is_client=True)
    configuration.verify_mode = False  # Disable certificate verification for testing

    # Establish the QUIC connection
    async with connect(
        host,
        port,
        configuration=configuration,
        session_ticket_handler=lambda _: None,
    ) as protocol:
        assert isinstance(protocol, QuicConnectionProtocol)
        request_headers = [
            (":method", "GET"),
            (":scheme", "https"),
            (":authority", host),
            (":path", parsed_url.path or "/"),
        ]

        # Perform the request
        stream_id = protocol._quic.get_next_available_stream_id()
        protocol._quic.send_headers(stream_id, request_headers, end_stream=True)

        # Collect the response
        response = await protocol._receive_response(stream_id)
        return response.decode()

        
# Tester la fonction
if __name__ == "__main__":
    url = "https://cloudflare-quic.com/"  # URL compatible HTTP/3 pour tester
    response = asyncio.run(download_http3(url))
    print("Réponse HTTP/3 :", response[:200])  # Afficher les 200 premiers caractères

