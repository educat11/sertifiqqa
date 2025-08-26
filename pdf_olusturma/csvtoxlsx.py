import pandas as pd

def csv_excel_donustur():
    # CSV dosyasını okuma
    csv_file = '../liste/etkinlik.csv'  # CSV dosyanızın adı ve yolu
    df = pd.read_csv(csv_file)

    # DataFrame'i Excel dosyasına kaydetme
    excel_file = 'etkinlik.xlsx'  # Oluşacak Excel dosyasının adı ve yolu
    df.to_excel(excel_file, index=False, engine='openpyxl')

    print(f"{csv_file} başarıyla {excel_file} dosyasına dönüştürüldü.")
