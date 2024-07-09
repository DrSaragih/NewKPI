import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.title("Sistem Scoring KPI untuk Unpar")
st.subheader("Berdasarkan Kriteria Malcolm Baldrige")

# CSS Custom untuk radio buttons mendatar
st.markdown(
    """
    <style>
    .stRadio > div {
        flex-direction: row;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Inisialisasi session state untuk subtopik yang telah selesai
if 'completed_topics' not in st.session_state:
    st.session_state.completed_topics = []
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

# Definisikan kriteria dan subtopik beserta pertanyaan
kriteria = {
    "Leadership": {
        "Senior Leadership": {
            "Visi, Misi dan Nilai":[
                "Bagaimana senior leader menciptakan visi dan nilai??",
                "Bagaimana senior leader menanamkan visi dan nilai pada sistem kepemimpinan, kepada pemasok , kepada mitra dan pemasok , dan kepada pasien ataupun stakeholder dengan sesuai?",
                "Bagaimana aksi mereka dalam mencerminkan komitmen terhadap nilai organisasi?",
                "Bagaiamana mereka mendemonstrasikan komitmen mereka terhadap hukum dan etika perilaku?",
                "Bagaimana mereka meningkatkan lingkungan organisasi yang sesuai untuk itu?",
                "Bagaimana mereka menciptakan sebuah organisasi yang terus berkelanjutan?"
            ],
            "Komunikasi dan Performa Organisasi":[
                "Bagaimana para senior leader berkomunikasi dan peran keterlibatannya dengan seluruh tenaga kerja?",
                "Bagaiamana mereka menciptakan fokus di tindakan untuk mencapai tujuan, meningkatkan performa dan meraih visinya?",
                "Bagaimana mereka mengidentifikasi langkah apa saja yang diperlukan?",
                "Bagaimana mereka menyisipkan fokus pada saat menciptakan dan menyeimbangkan nilai bagi pasien dan stakeholder lainnya di ekspektasi performa organisasi mereka?"
            ]
        },
        "Governance and Societal responsibilities": {
            "Pemerintahan Organisasi":[
                "Bagaimana Organisasi anda mereview dan meraih beberapa aspek seperti, Akuntabilitas dan langkah manajemen Akuntabilitas fiskal dan kemandirian dalam melaksanakan internal dan eksternal audit?",
                "Bagaimana anda mengevaluasi performa dari para senior leader, termasuk CEO?",
                "Bagaimana Anda menggunakan evaluasi kinerja dalam menentukan kompensasi eksekutif?",
            ],
            "Hukum dan Etika Perilaku":[
                "Bagaimana Anda mengatasi dampak negatif pada masyarakat dalam pelayanan perawatan kesehatan dan operasi?",
                "Bagaimana Anda mengantisipasi keprihatinan publik terhadap jasa dan operasi untuk saat ini dan masa depan?",
                "Bagaimana organisasi Anda mempromosikan dan memastikan perilaku etis dalam semua interaksi?",
            ],
            "Tanggung Jawab kepada masyarakat dan Dukungan Masyarakat kunci":[
                "Bagaimana Anda mempertimbangkan sosial dengan baik-makhluk dan manfaat sebagai bagian dari strategi Anda dan harian operasi?",
                "Bagaimana organisasi Anda secara aktif mendukung dan memperkuat komunitas kunci Anda?",
            ],
        },
    },
    "Strategic Planning": {
        "Proses Pengembangan Strategi": {
            "Pengembangan Strategi":[
                "Bagaimana senior leader menciptakan visi dan nilai??",
                "Bagaimana senior leader menanamkan visi dan nilai pada sistem kepemimpinan, kepada pemasok , kepada mitra dan pemasok , dan kepada pasien ataupun stakeholder dengan sesuai?",
                "Bagaimana aksi mereka dalam mencerminkan komitmen terhadap nilai organisasi?",
                "Bagaiamana mereka mendemonstrasikan komitmen mereka terhadap hukum dan etika perilaku?",
                "Bagaimana mereka meningkatkan lingkungan organisasi yang sesuai untuk itu?",
                "Bagaimana mereka menciptakan sebuah organisasi yang terus berkelanjutan?"
            ],
            "Tujuan strategis":[
                "Bagaimana para senior leader berkomunikasi dan peran keterlibatannya dengan seluruh tenaga kerja?",
                "Bagaiamana mereka menciptakan fokus di tindakan untuk mencapai tujuan, meningkatkan performa dan meraih visinya?",
                "Bagaimana mereka mengidentifikasi langkah apa saja yang diperlukan?",
                "Bagaimana mereka menyisipkan fokus pada saat menciptakan dan menyeimbangkan nilai bagi pasien dan stakeholder lainnya di ekspektasi performa organisasi mereka?"
            ],
        },
        "Implementasi Strategi": {
            "Rencana Aksi Pengembangan dan Penyebaran":[
                "Bagaimana Anda mengembangkan rencana aksi Anda?",
                "Apa kunci jangka pendek dan jangka panjang rencana aksi dan hubungan mereka dengan tujuan strategis Anda?",
                "Bagaimana Anda menyebarkan rencana aksi di seluruh organisasi untuk tenaga kerja Anda dan pemasok utama, mitra, dan kolaborator dengan sebagaimana mestinya, untuk mencapai tujuan utama strategis Anda?",
                "Bagaimana mereka mendemonstrasikan komitmen mereka terhadap hukum dan etika perilaku?",
                "Bagaimana Anda memastikan bahwa sumber daya keuangan dan lainnya yang tersedia untuk mendukung pemenuhan rencana tindakan Anda, sementara memenuhi kewajiban saat ini?",
                "Apa sumber daya kunci daya manusia atau tenaga kerja untuk mencapai rencana Anda pendek dan jangka panjang tujuan strategis dan rencana aksi?",
                "Apa ukuran kinerja kunci atau indikator untuk melacak pencapaian dan efektivitas rencana tindakan Anda?",
                "Bagaimana Anda membangun dan mengimplementasikan rencana aksi yang diubah jika keadaan memerlukan perubahan dalam rencana dan pelaksanaan yang cepat dari rencana baru?"
            ],
        },
    },
    "Customer Focus": {
        "Suara Kustomer": {
            "Mendengarkan Pasien dan Stakeholder":[
                "Bagaimana Anda mendengarkan pasien dan pemangku kepentingan untuk mendapatkan informasi yang dapat ditindaklanjuti?",
                "Bagaimana metode Anda mendengarkan kelompok pasien yang berbeda, kelompok stakeholder, atau segmen pasar yang bervariasi?",
                "Bagaimana Anda mendengarkan mantan pasien dan stakeholder, pasien potensial dan stakeholde, dan pasien pesaing dan stakeholder untuk memperoleh informasi yang dapat ditindaklanjutin dan untuk mendapatkan umpan balik pasien, dukungan stakeholder, dan transparasi, yang sesuai?",
            ],
            "Determinan Kepuasan dan Keterlibatan Pasien dan Stakeholder":[
                "Bagaimana Anda menentukan deteminan kepuasan dan keterlibatan pasien dan stakeholder?",
                "Bagaimana perbedaan metode penentuan antara kelompok pasien dan stakeholder dan segmen pasar yang tepat?",
                "Bagaimana Anda memperoleh informasi tentang kepuasan pasien Anda dan stakeholder relatif terhadap kepuasan mereka dengan pesain Anda?",
                "Bagaimana Anda menentukan ketidakpuasan pasien dan stakeholder?"
            ],
        },
        "Customer Engagement":{
            "Penawaran Pelayanan Perawatan Kesehatan dan Dukungan Stakeholder":[
                "Bagaimana Anda mengidentifikasi pasien, pemangku kepentingan, dan kebutuhan pasar untuk penawaran layanan kesehatan?",
                "Bagaimana Anda mengidentifikasi dan berinovasi tentang penawaran layanan untuk memenuhi persayratan dan melebihi harapan pasien dan kelompok pemangku kepentingan dan segemen pasar(diidentifikasi dalam Profil Organisasi Anda)?",
                "Bagaimana Anda mengaktifkan pasien dan pemangku kepentingan untuk mencari informasi dan dukungan?",
                "Bagaimana Anda memungkinkan mereka untuk mendapatkan pelayanan kesehatan dari Anda dan memberikan umpan balik pada layanan dan dukungan Anda?"
            ],
            "Membangun Hubungan dengan Pasien dan Stakeholder":[
                "Bagaimana Anda membangun pasar, dan mengelola hubungan dengan pasien dan stakeholder untuk mencapai nilai pasar yang baik?",
                "Bagaimana Anda mengelola keluhan pasien dan pemangku kepentingan?",
                "Bagaimana proses manajemen komplain pasien Anda dan pemangku kepentingan untuk memastikan bahwa pengaduan yang diajukan diselesaikan segera dan efektif?",
                "Bagaimana proses manajemen komplain pasien Anda dan pemangku kepentingan meyakinkan mereka untuk mengembalikan kepercayaan, dan keyakinan stakeholder dan menungkatkan kepuasan dan keterlibatan mereka?", 
            ],
        },
    },
    "Measurement, Analysis, and Knowledge Management": {
        "Pengukuran, Analisis, dan Peningkatan Kinerja Organisasi": {
            "Pengukuran Kinerja":[
                "Bagaimana memilih, mengumpulkan, menyelaraskan, dan mengintegrasikan data dan informasi untuk menelurusi operasional sehari-hari dan kinerja organisasi secara keseluruhan? (termasuk kemajuan yang berhubungan dengan tujuan strategis dan rencana teknis)",
                "Apa ukuran ukuran kunci kinerja organisasi, termasuk ukuran kunci jangka pendek dan jangka panjang finansial?",
                "Seberapa sering mengevaluasi ukuran tersebut?",
                "Bagaimana menggunakan data dan informasi untuk mendukung pengambilan keputusan organisasi dan inovasi?",
            ],
            "Analisis Kinerja dan Peninjauan Kembali":[
                "Bagaimana meninjau kinerja organisasi dan kemampuan?",
                "Bagaimana menggunakan ukuran kunci kinerja organisasi dalam proses tinjauan?",
                "Apa analisis yang dilakukan untuk mendukung tinjauan dan memastikan bahwa kesimpulan telah valid?",
                "Bagaimana menggunakan tinjauan untuk menilai keberhasilan organisasi, kinerja yang kompetitif, kesehatan keuangan, dan kemajuan sehubungan dengan tujuan strategis dan rencana aksi?"
            ],
            "Peningkatan Kinerja":[
                "Bagaimana menggunakan temuan tinjauan kinerja untuk berbagi pelajaran dan praktik terbaik (best practice) di seluruh unit organisasi dan proses kerja?",
                "Bagaimana menggunakan temuan tinjauan kinerja dan data komparatif dan kompetitif kunci untuk memproyeksikan kinerja masa depan?",
                "Bagaimana menggunakan temuan tinjauan kinerja organisasi untuk mengembangkan prioritas untuk perbaikan berkelanjutan dan peluang untuk mengembangkan inovasi?",
                "Bagaimana prioritas dan peluang dikerahkan untuk kelompok kerja dan operasional tingkat fungsional di seluruh organisasi?",
            ],
        },
        "Manajemen Teknologi Informasi, Pengetahuan, dan Informasi":{
            "Data, Informasi, dan Manajemen Pengetahuan":[
                "Bagaimana mengelola data organisasi, informasi, dan pengetahuan untuk memastikan ketepatan, integritas dan kehandalan?",
                "Bagaimana membuat data dan informasi yang diperlukan tersedia untuk tenaga kerja, pemasok, mitra, kolaborator, pasien, dan stakeholder?",
                "Bagaimana mengelola pengetahuan organisasi untuk mencapai kestabilan tersebut?",
            ],
            "Manajemen Sumber Daya Informasi dan Teknologi":[
                "Bagaimana memastikan bahwa hardware dan software telah handal, aman, dan user friendly?",
                "Dalam keadaan darurat, bagaimana memastikan ketersediaan lanjutan hardware dan sistem perangkat lunak dan ketersediaan lanjutan dari data dan informasi agar tetap dapat secara efektif melayani pasien, pemangku kepentingan, dan kebutuhan organisasi?",
            ],
        },
    },
    "Workforce Focus": {
        "Lingkungan Tenaga Kerja": {
            "Tenaga Kerja, Kemampuan, dan Kapasitas":[
                "Bagaimana menilai kebutuhan kemampuan dan kapasitas tenaga kerja, termasuk keterampilan, kompetensi, dan tingkat staff?",
                "Bagaimana merekrut, mempekerjakan, menempatkan dan mempertahankan anggota tenaga kerja baru?",
                "Bagaimana memastikan bahwa tenaga kerja yang ada telah merepresentasikan ide, budaya, dan pemikiran yang beragam dari perekrutan dan komunitas pasien dan pemangku kepentingan?",
                "Bagaimana mempersiapkan tenaga kerja pada saat mengubah kebutuhan kemampuan dan kapasitas?",
            ],
            "Iklim Tenaga Kerja":[
                "Bagaimana mengatasi faktor atau isu lingkungan tempat kerja, termasuk aksesibilitas, untuk menjamin dan meningkatkan kesehatan, keselamatan, dan keamanan tenaga kerja?",
                "Apa ukuran kinerja dan tujuan perbaikan untuk masing-masing kebutuhan tenaga kerja?",
                "Apa perbedaan signifikan pada faktor faktor tersebut dan ukuran kinerja atau target untuk lingkungan tempat kerja yang berbeda?",
                "Bagaimana mendukung tenaga kerja organisasi melalui implementasi kebijakan, layanan, dan manfaat?",
                "Bagaimana hal tersebut disesuaikan dengan kebutuhan tenaga kerja yang beragam dan kelompok dan segmen tenaga kerja yang berbeda?",
            ],
        },
        "Keterlibatan Tenaga Kerja":{
            "Kinerja Tenaga Kerja":[
                "Bagaimana menentukan elemen kunci yang mempengaruhi keterlibatan tenaga kerja?",
                "Bagaimana menentukan elemen kunci yang mempengaruhi kepuasan tenaga kerja?",
                "Bagaimana menentukan unsur-unsur untuk kelompok dan segmen tenaga kerja yang berbeda?",
                "Bagaimana menumbuhkan budaya organisasi yang dikarakteristikkan dengan komunikasi terbuka, kinerja tinggi, dan tenaga kerja yang terlibat?",
            ],
            "Penaksiran Keterlibatan Tenaga Kerja":[
                "Bagaimana menaksir keterlibatan tenaga kerja?",
                "Apa metode penaksiran formal dan informal dan ukuran yang digunakan untuk menentukan keterlibatan dan kepuasan tenaga kerja?",
                "Bagaimana metode dan ukuran menjadi berbeda antar kelompok dan segmen tenaga kerja?",
                "Bagaimana menggunakan indikator lainnya, seperti retensi tenaga kerja, absensi, keluhan, keamanan, dan produktivitas, untuk menilai dan meningkatkan keterlibatan tenaga kerja?",
            ],
            "Pengembangan Tenaga Kerja dan Pemimpin":[
                "Bagaimana mengevaluasi efektivitas dan efisiensi sistem pembelajaran dan pengembangan?",
                "Bagaimana mengelola kemajuan karir yang efektif untuk seluruh tenaga kerja ?",
                "Bagaimana mencapai perencanaan suksesi yang efektif untuk posisi manajemen dan kepemimpinan?",
            ],
        },
    },
    "Operation Focus": {
        "Sistem Kerja": {
            "Rancangan Kerja":[
                "Bagaimana anda merancang dan meningkatkan sistem kerja secara keseluruhan?",
                "Bagaimana anda memanfaatkan kompetensi inti?",
                "Bagaimana Anda menentukan kunci kebutuhan sistem kerja, dan menggabungkan masukan dari pasien, stakeholder,pemasok, dan mitra secara sesuai?",
                "Apa yang menjadi kunci kebutuhan dari sistem kerja tersebut?",
            ],
            "Manajemen Sistem Kerja":[
                "Apa sistem kerja organisasi anda?",
                "Bagaimana anda mengatur dan meningkatkan sistem kerja untuk menyampaikan nilai kepada pasien dan stakeholder serta mencapai kesuksesan dan keberlanjutan organisasi?",
                "Bagaimana anda mengendalikan keseluruhan pengeluaran dari sistem kerja anda?",
                "Bagaimana anda mencegah dua kali kerja dan kesalahan, termasuk kesalahan medis dan hal-hal lain yang membahayakan pasien?",
                "Bagaimana Anda memperkecil biaya dari proses kinerja audit secara sesuai?",
            ],
            "Katanggapan Darurat":[
                "Bagaimana anda memastikan sistem kerja dan persiapan tempat kerja apabila  terjadi bencana dan keadaan darurat?",
                "Bagaimana sistem persiapan bencana dan keadaan darurat anda mempertimbangkan pencegahan,pengaturan, keberlangsungan dari operasi pasien, pengungsian, dan pemulihan?",
            ],
        },
        "Proses Kerja":{
            "Rancangan Proses Kerja":[
                "Bagaimana anda merancang dan meningkatkan proses kerja anda agar sesuai dengan semua kunci kebutuhan?",
                "Bagaimana Anda menggabungkan teknologi baru, pengetahuan akan organisasi, pengobatan berdasarkan bukti, pelayanan kesehatan yang unggul, dan potensi kelincahan ke dalam proses tersebut?",
                "Bagaimana anda menggabungkan siklus waktu, prokdutivitas, penguasaan biaya, dan faktor efektifitas serta efisiensi lainnya ke dalam proses tersebut?",
                "Bagaimana anda menentukan kebutuhan proses kunci?",
                "Apa yang menjadi proses kunci dari kinerja organisasi?",
                "Apa yang menjadi kebutuhan kunci dari proses kerja tersebut?",
            ],
            "Pengaturan Sistem Kerja":[
                "Bagaimana anda menghubungkan antara proses kunci dalam kerja dengan sistem kerja?",
                "Bagaimana anda memastikan bahwa operasi yang dilakukan sehari-hari memenuhi kebutuhan proses kunci?",
                "Apa kunci pengukuran kinerja atau indikator dalam proses untuk mengendalikan dan meningkatkan proses kerja anda?",
                "Bagaimana anda menyampaikan dan mempertimbangkan keinginan pasien?",
                "Bagaimana pelayanan kesehatan membawakan proses dan menjelaskan hasil untuk mengeset harapan realistis pasien",
                "Bagaimana faktor prefensi yang menyebabkan pasien mengambil keputusan untuk menuju ke layanan kesehatan?",
                "Bagaimana anda mengatur rantai penyediaan?", 
                "Bagaimana anda memastikan bahwa penyedia yang terpilih berkualifikasi dan ditempatkan untuk meningkatkan kinerja anda sehingga pasien dan stakeholder merasa puas?",
                "Bagaimana anda mengevaluasi kinerja penyedia?",
                "Bagaimana anda meningkatkan proses kerja dan mengurangi variabilitas untuk mencapai kinerja yang lebih baik sehingga hasil layanan kesehatan juga meningkat?",
            ],
        },
    },
    "Result": {
        "Health Care and Process Outcomes: what are your health care and process effectiveness result?": {
            "Hasil kefokusan terhadap pasien layanan kesehatan":[
                "Bagaimana tingkat dan tren anda berdasar indikator layanan kesehatan dan kinerja yang penting untuk dan langsung baik pada pasien maupun",
                "Bagaimana tingkat perbandingan hasil tersebut dengan kompetitor atau organisasi dibidang yang sama dengan anda?",
            ],
            "Hasil kefektifan proses operasional":[
                "Bagaimana tingkat dan tren anda berdasar indikator kinerja operasional yang menyangkut produktivitas, waktu dan faktor lain seperti efektifitas, efisiensi dan inovasi?",
                "Bagaimana tingkat dan tren anda berdasar indikator efektivitas sistem kerja anda dan persiapan untuk menghadapi bencana maupun kedaan yang bersifat darurat?",
            ],
            "Hasil pelaksanaan strategi":[
                "Bagaimana tingkat dan tren anda berdasar indikator pencapaian dari strategi organisasi dan rencana aksi, yang termasuk didalamnya membangun dan meningkatkan kompetensi inti?",
            ],
        },
        "Customer-Focused Outcomes : What are your patient and stakeholderfocused performance results?":{
            "Hasil Kefokusan terhadap pelanggan":[
                "Bagaimana tingkat dan tren anda berdasar indikator dari kepuasan dan ketidakpuasan pasien maupun stakeholder yang ada?",
                "Bagaimana tingkat dan tren anda berdasar indikator dari keterlibatan pasien maupun stkeholder yang ada dalam membangun hubungan?",
            ],
        },
        "Workforce-focused Outcomes : What are your workforce focused performance results?":{
            "Hasil dari tenaga kerja":[
                "Bagaimana tingkat dan tren anda berdasar indikator dari kemampuan dan kapasitas tenaga kerja, misalnya dalam ketrampilan dan tingkat staf yang sesuai?",
                "Bagaimana tingkat dan tren anda berdasar indikator pengembangan tenaga kerja dan pemimpin?",
            ],
        },
        "Leadership and Governance Outcomes : What are your senior leadership and governance results?":{
            "Hasil pemerintahan dan tanggung jawab sosial":[
                "Bagaimana tingkat dan tren anda berdasar indikator keterlibatan dan komunikasi dar i pemimpin senior dengan tenaga kerja untuk menyebarkan visi dan nilai, mendorong komunikasi 2 arah dan melakukan tindakan yang fokus?",
                "Bagaimana tingkat dan tren anda berdasarkan  indikator pencapaian dan penilaian hukum dan persyaratan akreditasi?",
            ],
        },
        "Financial and Market Outcomes: What are your financial and marketplace performance results?":{
            "Hasil keuangan dan pasar":[
                "Bagaimana tingkat dan tren anda berdasar indikator kinerja keuangan termasuk sgregat pengembalian keuangan, kinerja anggaran yang tepat?",
                "Bagaimana tingkat dan tren anda berdasar indikator pasar kinerja, termasuk pangsa pasar, pertumbuhan pangsa pasar dan pasar baru yang sesuai?",
            ],
        },
    },
    # Tambahkan kriteria lainnya sesuai kebutuhan
}

bobot_poin = {
    'Leadership': 120,
    'Strategic Planning': 85,
    'Customer Focus': 85,
    'Measurement, Analysis, and Knowledge Management': 90,
    'Workforce Focus': 85,
    'Operation Focus': 85,
    'Result': 450
}

# Fungsi untuk menghitung nilai akhir
def calculate_final_score(responses, bobot_poin):
    final_score = 0
    category_scores = {}
    for kategori, subtopiks in responses.items():
        kategori_score = 0
        for subtopik, subsubtopiks in subtopiks.items():
            subtopik_score = 0
            total_questions = 0
            for subsubtopik, questions in subsubtopiks.items():
                for question, answer in questions.items():
                    subtopik_score += answer['score']
                    total_questions += 1
            subtopik_score /= total_questions
            kategori_score += subtopik_score
        kategori_score /= len(subtopiks)
        category_scores[kategori] = kategori_score * bobot_poin[kategori.split(' ')[0]] / 100
        final_score += category_scores[kategori]
    return final_score, category_scores

# Simpan jawaban di session state agar tetap ada saat berpindah halaman
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'completed_topics' not in st.session_state:
    st.session_state.completed_topics = set()
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'personal_info' not in st.session_state:
    st.session_state.personal_info = {}

# Ikon untuk navigasi sidebar
menu_icons = {
    "Data Diri": "👤",
    "Isi Penilaian": "📝",
    "Hasil Akhir": "📊"
}

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
selected_page = st.sidebar.radio("Pilih Halaman", ["Data Diri", "Isi Penilaian", "Hasil Akhir"], format_func=lambda page: f"{menu_icons[page]} {page}")

# Halaman Data Diri
if selected_page == "Data Diri":
    st.header("Data Diri")
    st.session_state.personal_info['Nama'] = st.text_input("Nama", value=st.session_state.personal_info.get('Nama', ''))
    st.session_state.personal_info['Nomor Induk Pegawai'] = st.text_input("Nomor Induk Pegawai", value=st.session_state.personal_info.get('Nomor Induk Pegawai', ''))
    st.session_state.personal_info['Direktorat'] = st.text_input("Direktorat", value=st.session_state.personal_info.get('Direktorat', ''))
    st.session_state.personal_info['Jabatan'] = st.text_input("Jabatan", value=st.session_state.personal_info.get('Jabatan', ''))
    if st.button("Simpan Data Diri"):
        st.success("Data diri telah disimpan!")

# Halaman Isi Penilaian
elif selected_page == "Isi Penilaian":
    selected_kategori = st.sidebar.selectbox("Pilih Kategori", list(kriteria.keys()))
    selected_subtopik = st.sidebar.selectbox("Pilih Subtopik", list(kriteria[selected_kategori].keys()))

    st.sidebar.markdown("### Keterangan Nilai Relevansi")
    st.sidebar.markdown("""
    1 - Tidak sesuai\n
    2 - Kurang sesuai\n
    3 - Cukup sesuai\n
    4 - Sesuai\n
    5 - Sangat sesuai
    """)

    st.sidebar.markdown("### Topik yang Selesai")
    for kategori in st.session_state.completed_topics:
        st.sidebar.markdown(f"- ✅ {kategori}")

    # Tampilkan pertanyaan dan simpan jawaban
    responses = st.session_state.responses

    st.header(selected_kategori)
    st.subheader(selected_subtopik)
    responses[selected_kategori] = responses.get(selected_kategori, {})
    responses[selected_kategori][selected_subtopik] = responses[selected_kategori].get(selected_subtopik, {})

    for subsubtopik_name, questions in kriteria[selected_kategori][selected_subtopik].items():
        st.write(f"**{subsubtopik_name}**")
        responses[selected_kategori][selected_subtopik][subsubtopik_name] = responses[selected_kategori][selected_subtopik].get(subsubtopik_name, {})
        for idx, question in enumerate(questions):
            st.write(f"{idx + 1}. {question}")
            default_score = responses[selected_kategori][selected_subtopik][subsubtopik_name].get(question, {}).get('score', 50)
            default_relevance = responses[selected_kategori][selected_subtopik][subsubtopik_name].get(question, {}).get('relevance', 3)
            score = st.number_input(f"Nilai", min_value=0, max_value=100, value=default_score, step=1, key=f"{selected_kategori}_{selected_subtopik}_{subsubtopik_name}_{idx}_score")
            relevance = st.radio(f"Seberapa relevan pertanyaan ini dengan bidang anda?", [1, 2, 3, 4, 5], index=default_relevance-1, key=f"{selected_kategori}_{selected_subtopik}_{subsubtopik_name}_{idx}_relevance")
            responses[selected_kategori][selected_subtopik][subsubtopik_name][question] = {"score": score, "relevance": relevance}

    st.session_state.responses = responses

    # Tombol submit dan penandaan topik yang selesai
    if st.button("Submit"):
        st.session_state.completed_topics.add((selected_kategori, selected_subtopik))
        st.success(f"Topik {selected_subtopik} pada kategori {selected_kategori} telah disubmit!")

    # Check if all topics are completed to show final results
    if len(st.session_state.completed_topics) == sum(len(topiks) for topiks in kriteria.values()):
        st.session_state.show_results = True

# Halaman Hasil Akhir
elif selected_page == "Hasil Akhir" and st.session_state.show_results:
    st.header("Hasil Akhir")
    final_score, category_scores = calculate_final_score(st.session_state.responses, bobot_poin)
    
    st.write("Nilai Akhir Anda adalah:")
    score_data = {k: f"{v:.2f}" for k, v in category_scores.items()}
    score_data["Total"] = f"{final_score:.2f} dari 1000"
    st.table(score_data)
else:
    st.write("Selesaikan semua penilaian terlebih dahulu untuk melihat hasil akhir.")
