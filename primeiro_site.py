import subprocess
import streamlit as st
import os
import re
import tempfile
import psutil
import shutil
import streamlit as st
from tqdm import tqdm


def buscar_nome(nome, texto):
    padrao = r'\b{}\b'.format(re.escape(nome))
    ocorrencias = re.findall(padrao, texto, re.IGNORECASE)
    return len(ocorrencias) > 0

def download_facebook_video(url, output_format, progress_bar):
    cmd = f"youtube-dl -f {output_format} --newline {url}"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    for line in process.stdout:
        if " ETA " in line:
            progress = re.search(r"\d+(\.\d+)?%", line)
            if progress:
                progress_value = float(progress.group().strip("%")) / 100
                progress_bar.progress(progress_value)

    process.wait()


def download_page():
    video_url = st.text_input('URL do vídeo')
    output_format = st.selectbox('Formato de saída', ['mp4', 'mkv', 'avi'])

    if st.button('Baixar'):
        if video_url:
            st.info('Fazendo o download... Por favor, aguarde.')
            progress_bar = st.progress(0.0)
            download_facebook_video(video_url, output_format, progress_bar)
            st.success('O vídeo foi baixado com sucesso!')
        else:
            st.warning('Por favor, insira um URL válido.')


def pagina_busca():
    st.title("Página de Busca")
    
    texto_jornal = st.text_area("Cole o conteúdo do jornal aqui")
    nome_procurado = st.text_input("Digite o nome a ser procurado")
    buscar_botao = st.button("Buscar")

    if buscar_botao:
        if buscar_nome(nome_procurado, texto_jornal):
            st.write("O nome foi encontrado no jornal.")
        else:
            st.write("O nome não foi encontrado no jornal.")


def clean_prefetch_files():
    prefetch_folder = 'C:\\Windows\\Prefetch'
    removed_files = []

    file_count = sum(len(files) for _, _, files in os.walk(prefetch_folder))

    progress_bar = st.progress(0)
    cancel_event = st.button('Cancelar Limpeza')

    if cancel_event:
        st.warning('Limpeza de arquivos de prefetch cancelada.')
        return

    with tqdm(total=file_count, ncols=80, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
        for root, _, files in os.walk(prefetch_folder):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    removed_files.append(file_path)
                except PermissionError:
                    pass

                pbar.update(1)
                progress_bar.progress(pbar.n / pbar.total)

    for file_path in removed_files:
        st.write(file_path)


def clean_temp_files():
    temp_folder = tempfile.gettempdir()
    removed_files = []

    file_count = sum(len(files) for _, _, files in os.walk(temp_folder))

    progress_bar = st.progress(0)
    cancel_event = st.button('Cancelar Limpeza')

    if cancel_event:
        st.warning('Limpeza de arquivos temporários cancelada.')
        return

    with tqdm(total=file_count, ncols=80, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
        for root, _, files in os.walk(temp_folder):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    removed_files.append(file_path)
                except PermissionError:
                    pass

                pbar.update(1)
                progress_bar.progress(pbar.n / pbar.total)

    for file_path in removed_files:
        st.write(file_path)


def clean_system_files():
    try:
        process = subprocess.Popen(['cleanmgr', '/sagerun:1'], shell=True)
        progress_bar = st.progress(0)

        cancel_button = st.button('Cancelar Limpeza')
        while process.poll() is None:
            if cancel_button:
                process.terminate()
                st.warning('Limpeza de arquivos de sistema cancelada.')
                break

            progress_bar.progress(0.5)

        if not cancel_button:
            progress_bar.progress(1.0)
            st.success('Limpeza de arquivos de sistema concluída!')
    except Exception as e:
        st.error(f'Erro ao limpar os arquivos de sistema: {str(e)}')


def main():
    opcoes = ['Download de Vídeos do Facebook', 'Página de Busca', 'Limpeza de Arquivos']
    escolha = st.sidebar.selectbox('Selecione uma página', opcoes)

    if escolha == 'Download de Vídeos do Facebook':
        st.title('Download de Vídeos do Facebook')
        download_page()

    elif escolha == "Página de Busca":
        pagina_busca()

    elif escolha == 'Limpeza de Arquivos':
        st.title('Limpeza de Arquivos')
        st.write('Selecione o tipo de arquivo para limpar.')

        if st.button('Limpar Arquivos de Prefetch'):
            clean_prefetch_files()

        if st.button('Limpar Arquivos Temporários'):
            clean_temp_files()

        if st.button('Limpar Arquivos de Sistema'):
            clean_system_files()


if __name__ == '__main__':
    main()
