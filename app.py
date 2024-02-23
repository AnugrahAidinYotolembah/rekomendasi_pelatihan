import streamlit as st
import pandas as pd
import joblib
from streamlit_folium import folium_static
import folium





def get_recommendations(need, cosine_sim, data):
    search_recommendations = len(data)
    idx = data.loc[(data['need'] == need)].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:search_recommendations+1]
    company_indices = [i[0] for i in sim_scores]
    return data[['training_name']].iloc[company_indices].drop_duplicates()

def need_recommendation(need, data, cosine_sim):
    recommendations = get_recommendations(need, cosine_sim, data)[:10]
    recommendations['score'] = range(1, len(recommendations) + 1)
    recommendations_sorted = recommendations.sort_values(by='score', ascending=True)

    for i, row in recommendations_sorted.iterrows():
        score_percent = (len(recommendations) - row['score'] + 1) / len(recommendations) * 100
        result_string = f"{row['training_name']} (compatibility: {score_percent:.2f}%)"
        recommendations_sorted.loc[i, 'training_name'] = result_string

    recommendations_sorted = recommendations_sorted.drop(['score'], axis=1)
    dict_from_df = recommendations_sorted.to_dict(orient='list')
    return dict_from_df









# Fungsi utama
def main():
    st.set_page_config(page_title="Rekomendasi Produk Pelatihan", page_icon="/Users/didiyotolembah19gmail.com/Documents/magang/MKNOWS - CONSULTING AI & DATA SCIENCE MSIB 5/AI SALES/model 1/deploy/sistemrekomendasi_pelatihan/image/artificial-intelligence (1) (1).png", layout="wide", initial_sidebar_state="collapsed", menu_items=None)
    # Mengatur warna latar belakang menjadi putih
    page_bg_img = '''
    <style>
    body {
    background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
    background-size: cover;
    }
    footer {visibility: hidden;}
    @media only screen and (max-width: 600px) {
    /* Atur gaya tata letak untuk layar seluler */
    body {
    background-image: none;  /* Hapus gambar latar belakang untuk layar seluler */
    background-color: #ffffff;  /* Ganti latar belakang dengan warna putih */ 
    }
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)


    # Menambahkan sidebar dengan foto, nama, dan nim
    def home_page():
        st.title("Home")
        st.title("Selamat Datang Kembali")
            
        
    def profile_page():
        st.title("Profile")
        st.image("image/Anugrah Aidin Yotolembah_F55120093.jpg", use_column_width=True)
        st.title("Anugrah Aidin Yotolembah")
        st.title("F55120093")
        st.title("S1 Teknik Informatika")
        st.title("Universitas Tadulako")

    with st.sidebar:
        selected = st.selectbox(" ", ["Home", 'Profile'], index=0) 
        

        if selected == "Home":
            home_page()
        elif selected == "Profile":
            profile_page()

    # Judul halaman dengan warna dan style
    st.markdown(
        """
        <h2 style='text-align: center; color: #FFFFFF;'>Implementasi Sistem Rekomendasi Penjualan produk Pelatihan Terbaik menggunakan algoritma Cosine Similarity<br>(studi kasus : PT MENARA INDONESIA)</h2>
        <hr style='border: 2px solid #182c25;'>
        <br>
        <h2 style='text-align: center; color: #FFFFFF;'>Katalog Penjualan Pelatihan</h2>
        <br>
        """,
        unsafe_allow_html=True
    )

    image_path1 = "image/gambar_1.png"  # Ganti dengan path gambar yang sesuai
    st.image(image_path1, use_column_width=True)
    image_path2 = "image/gambar_2.png"  # Ganti dengan path gambar yang sesuai
    st.image(image_path2, use_column_width=True)
    image_path3 = "image/gambar_3.png"  # Ganti dengan path gambar yang sesuai
    st.image(image_path3, use_column_width=True)
    image_path4 = "image/gambar_4.png"  # Ganti dengan path gambar yang sesuai
    st.image(image_path4, use_column_width=True)
   
    # Visualisasi peta Indonesia dengan folium
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #FFFFFF;'>daerah pelatihan yang telah dikunjungi</h2>", unsafe_allow_html=True)
        
    # Contoh peta statis menggunakan folium
    m = folium.Map(location=[-2.5489, 118.0149], zoom_start=5)  # Koordinat tengah Indonesia

    # Menambahkan marker pada peta (contoh)
    folium.Marker([-6.2088, 106.8456], popup='Jakarta').add_to(m)
    folium.Marker([-7.2504, 112.7688], popup='Surabaya').add_to(m)
    folium.Marker([-6.595038, 106.816635], popup='Bogor').add_to(m)
    folium.Marker([-6.966667, 110.416664], popup='Semarang').add_to(m)
    folium.Marker([-6.347891, 106.741158], popup='Tangerang Selatan').add_to(m)
    folium.Marker([1.474830, 124.842079], popup='Manado').add_to(m)
    folium.Marker([-6.905977, 107.613144], popup='Bandung').add_to(m)
    folium.Marker([-1.609972, 103.607254], popup='Jambi').add_to(m)
    folium.Marker([-7.797068, 110.370529], popup='Yogyakarta').add_to(m)
    folium.Marker([-6.966667, 110.416664], popup='Semarang').add_to(m)
    folium.Marker([-6.178306, 106.631889], popup='Tangerang').add_to(m)
    

    # Menampilkan peta
    # Menampilkan peta dengan responsif
    folium_static(m, width=940, height=500)

    make_map_responsive= """
        <style>
        [title~="st.iframe"] { width: 100%}
        </style>
        """
    st.markdown(make_map_responsive, unsafe_allow_html=True)
    
    st.markdown(
        """
        <hr style='border: 2px solid #182c25;'>
        <br>
        <h2 style='text-align: center; color: #FFFFFF;'>Rekomendasi Produk Pelatihan Terbaik</h2>
        """,
        unsafe_allow_html=True
        )


    # Pilihan list up-down untuk kebutuhan pelatihan
    options= [
    "Mampu Analisa Data yang Mendalam",
    "Membuat Platform Big Data yang Tangguh",
    "Keterampilan Analisis Data yang Mendalam",
    "Keterampilan Integrasi Data yang Lengkap",
    "Analisa Kepatuhan dan Keamanan Data",
    "Peningkatan Keterampilan dalam Pemasaran dan Penjualan",
    "Dukungan Administrasi Penjualan yang Efektif",
    "Pengembangan Tim Marketing Support dan Pemimpin",
    "Peningkatan Dukungan Pemasaran",
    "Penyelarasan antara Tim Pemasaran dan Penjualan",
    "Pengetahuan Mendalam tentang Produk dan Layanan Financial",
    "Kemampuan Digital Marketing yang Kuat",
    "Analisis Digital Marketing yang Mendalam",
    "Platform Teknologi yang Fleksibel",
    "Kepatuhan dan Keamanan",
    "Strategi Digital Marketing yang Terarah",
    "Kemampuan membuat Konten Berkualitas dan Relevan",
    "Kemampuan Optimisasi Pengalaman Bisnis",
    "Keterampilan Menganalisis Data untuk Pengambilan Keputusan",
    "Pengembangan Keterampilan Digital Marketing",
    "Kemampuan Strategi Branding yang Jelas",
    "Pengembangan Cerita Merek yang Menarik",
    "Penguasaan Platform Media Sosial",
    "Kemampuan Kreativitas dalam Konten Visual dan Narasi",
    "Keterampilan Analisis Kinerja dan Pengoptimalan",
    "Penargetan Audiens Bisnis yang Tepat",
    "Konten yang Berorientasi pada Bisnis",
    "Optimisasi SEO untuk Pencarian Bisnis B2B",
    "Kemampuan Penggunaan Media Sosial Profesional",
    "Kemampuan Analisis Data untuk Pengambilan Keputusan",
    "Kemampuan Penelitian Kata Kunci yang Mendalam untuk Bisnis",
    "Keterampulan Optimisasi SEO",
    "Peningkatan Pengalaman Pengguna SEO (Search Engine Optimization)",
    "Strategi Link Building yang Kuat untuk SEO (Search Engine Optimization) Bisnis",
    "Sistem Manajemen Pelanggan (CRM)",
    "Kemampuan Strategi Pemasaran Terintegrasi",
    "Keterampilan Pelatihan dan Pengembangan Karyawan",
    "Analisis Data untuk Pengambilan Keputusan",
    "Koordinasi antara Tim Penjualan dan Pemasaran",
    "Kreativitas dan Inovasi Produk",
    "Kemampuan Pelayanan Pelanggan yang Unggul",
    "Keterampilan Strategi Penjualan yang Kuat",
    "Analisis dan Pengukuran Kinerja",
    "Kepemimpinan yang Mengutamakan Inovasi",
    "Kemampuan Platform E-Commerce yang Optimal",
    "Strategi Pemasaran Digital yang Terarah",
    "Pengalaman Pengguna yang Memikat",
    "Keterampilan Penjualan dan Komunikasi Online",
    "Analisis Data dan Pengoptimalan",
    "Analisis Risiko dan Penilaian Aset",
    "Pengembangan Strategi Pemasaran",
    "Keterampilan Penjualan dan Negosiasi",
    "Kepatuhan Regulasi dan Hukum",
    "Pemahaman Pasar dan Tren",
    "Kemampuan Pelatihan Keterampilan Manajemen",
    "Pengembangan Tim yang Efektif",
    "Pemahaman yang Mendalam tentang Industri Koleksi",
    "Keterampilan Motivasi dan Penghargaan Tim",
    "Manajemen Perubahan dan Transformasi Keterampilan",
    "Akses Terhadap Laporan Keuangan",
    "Keterampilan Analisis Keuangan",
    "Keterampilan Mmempuan Kerangka Kerja Analisis Kredit",
    "Kemampuan Kepatuhan Terhadap Regulasi",
    "Keterampilan Komunikasi dan Kolaborasi",
    "Kemampuan Membuat Sistem Keamanan Dokumen yang Kuat",
    "Kemampuan Membuat Teknologi Verifikasi Tanda Tangan",
    "Pelatihan dan Kesadaran Karyawan",
    "Kemampuan membuat Sistem Deteksi Kecurangan",
    "Kerjasama dengan Otoritas Penegak Hukum",
    "Teknologi Verifikasi Tanda Tangan Digital",
    "Pengembangan Sistem Identifikasi Ciri Tulisan Tangan",
    "Pelatihan dan Pendidikan Karyawan",
    "Implementasi Kebijakan dan Prosedur Keamanan",
    "Kerjasama dengan Pihak Eksternal",
    "Keterampilan Kepatuhan Regulasi atas penagihan kartu kredit",
    "Pengembangan Kebijakan dan Prosedur",
    "Keterampilan Konsultasi Hukum",
    "KeterampilanPenanganan Perselisihan",
    "Pengelolaan Risiko Hukum",
    "Pelatihan Keterampilan Surveyor",
    "Pengembangan Keterampilan Credit Analyis",
    "Keterampilan Penyelesaian Masalah",
    "Kemampuan Manajemen Waktu",
    "Etika Profesional",
    "Kebijakan dan Prosedur Pencegahan Transaksi Pencucian Uang",
    "Keterampilan Pelatihan Karyawan untuk Pencegahan Transaksi Pencucian Uang",
    "Keterampilan Teknologi dan Sistem Informasi dalam Pencegahan Transaksi Pencucian Uang",
    "Kolaborasi dengan Otoritas",
    "Keterampilan Audit dan Evaluasi Berkelanjutan",
    "Pemahaman Hukum dan Peraturan",
    "Penyusunan Kebijakan dan Prosedur",
    "Pelatihan Karyawan",
    "Sistem Informasi Penagihan sesuai dengan PJOK 11 (3/2020)",
    "Kolaborasi dengan Otoritas Terkait",
    "Pelatihan Keterampilan Komunikasi in New Normal Era",
    "Pemahaman tentang Teknologi Komunikasi",
    "Keterampilan Manajemen Konflik",
    "Adaptasi terhadap Perubahan Perilaku Konsumen",
    "Kolaborasi dengan Otoritas Terkait"
]

      # Ganti dengan pilihan yang sesuai
    need = st.selectbox("Pilih kebutuhan pelatihan:", options)

    # Button untuk mendapatkan rekomendasi
    if st.button("Dapatkan Rekomendasi"):
        data = pd.read_csv('dataset/AISALES_FITUR-6rev (3).csv')
        cosine_sim = joblib.load('models/AISALES_FITUR6revterbaru (1).joblib')
        recommendations = need_recommendation(need, data, cosine_sim)

        # Menampilkan header dengan warna dan style
        st.markdown("<h2 style='color: #FFFFFF;'>Rekomendasi Pelatihan:</h2>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(
            """
            <style>
            table {
                color: #FFFFFF;
                background-color: #182c25;  /* Warna latar belakang tabel */
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Menampilkan rekomendasi dalam bentuk tabel
        st.table(pd.DataFrame(recommendations))

        


        

        
if __name__ == '__main__':
    main()