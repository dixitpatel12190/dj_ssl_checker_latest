from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from cryptography.x509 import load_pem_x509_certificate, ExtensionOID
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def handle_operation(request):
    if request.method == 'POST':
        operation = request.POST.get('handle_operation')
        if operation == 'verify_cert':
            return redirect('verify_cert')
        elif operation == 'decrypt_key':
            return redirect('decrypt_key')
        elif operation == 'verify_bundle':
            return redirect('verify_bundle')
    return redirect('/')

def verify_cert(request):
    analysed = ""
    if request.method == "POST":
        cert_file = request.FILES.get('cert_file')
        key_file = request.FILES.get('key_file')
        key_password = request.POST.get('key_password', '')
        if cert_file and key_file:
            try:
                cert_data = cert_file.read()
                key_data = key_file.read()
                from cryptography.hazmat.primitives import serialization
                from cryptography.x509 import load_pem_x509_certificate
                from cryptography.hazmat.backends import default_backend
       
                cert = load_pem_x509_certificate(cert_data, default_backend())
                password = key_password.encode() if key_password else None
                key = serialization.load_pem_private_key(key_data, password=password, backend=default_backend())
                if cert.public_key().public_numbers() == key.public_key().public_numbers():
                    analysed = "Certificate and Key match!"
                else:
                    analysed = "Certificate and Key do NOT match."

                # Extract certificate details
                common_name = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
                serial_number = cert.serial_number
                expiry_date = cert.not_valid_after

                # Extract SANs if present
                try:
                    san_extension = cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
                    san = san_extension.value.get_values_for_type(NameOID.DNS_NAME)
                except Exception:
                    san = []
                issuer = cert.issuer.rfc4514_string()
                index = issuer.find(',')
                if index != -1:
                   result = issuer[:index]
                else:
                   result = issuer

                params = {
                    'analysed_text1': analysed,
                    'common_name': common_name,
                    'serial_number': serial_number,
                    'expiry_date': expiry_date,
                    'issuer': result,
                    'san': san
                }
                return render(request, 'cert_result.html', params)
            except Exception as e:
                analysed = f"Error processing files: {e}"
                params = {'analysed_text1': analysed}
                return render(request, 'cert_result.html', params)
        else:
            analysed = "Please upload both certificate and key files."
            params = {'purpose': 'Certificate & Key Comparison', 'analysed_text1': analysed}
            return render(request, 'cert_result.html', params)
    return render(request, 'cert.html')


def decrypt_key(request):
    if request.method == "POST":
        key_file = request.FILES.get('key_file')
        key_password = request.POST.get('key_password', '')

        if not key_file:
            return render(request, 'decrypt_key.html', {'error': 'Please upload a private key file.'})

        key_data = key_file.read()
        password = key_password.encode() if key_password else None

        try:
            private_key = serialization.load_pem_private_key(key_data, password=password, backend=default_backend())

            decrypted_pem = private_key.private_bytes(
                encoding=Encoding.PEM,
                format=PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=NoEncryption()
            )

            response = HttpResponse(decrypted_pem, content_type='application/x-pem-file')
            response['Content-Disposition'] = 'attachment; filename="decrypted_private.key"'
            return response

        except Exception as e:
            # keep the page with an error message so the user can retry
            return render(request, 'decrypt_key.html', {'error': f'Error decrypting key: {e}'})
        
    return render(request, 'decrypt_key.html')


def verify_bundle(request):
    return redirect('https://redkestrel.co.uk/tools/decoder')