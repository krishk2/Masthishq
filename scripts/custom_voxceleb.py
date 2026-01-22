# coding=utf-8
# Copyright 2022 The HuggingFace Datasets Authors and Arjun Barrett.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""VoxCeleb audio-visual human speech dataset."""

import json
import os
from urllib.parse import urlparse, parse_qs
from getpass import getpass
from hashlib import sha256
from itertools import repeat
from multiprocessing import Manager, Pool, Process
from pathlib import Path
from shutil import copyfileobj
from warnings import catch_warnings, filterwarnings
from urllib3.exceptions import InsecureRequestWarning

import pandas as pd
import requests

import datasets

_CITATION = """\
@Article{Nagrani19,
    author = "Arsha Nagrani and Joon~Son Chung and Weidi Xie and Andrew Zisserman",
    title = "Voxceleb: Large-scale speaker verification in the wild",
    journal = "Computer Science and Language",
    year = "2019",
    publisher = "Elsevier",
}
@InProceedings{Chung18b,
    author = "Chung, J.~S. and Nagrani, A. and Zisserman, A.",
    title = "VoxCeleb2: Deep Speaker Recognition",
    booktitle = "INTERSPEECH",
    year = "2018",
}
@InProceedings{Nagrani17,
    author = "Nagrani, A. and Chung, J.~S. and Zisserman, A.",
    title = "VoxCeleb: a large-scale speaker identification dataset",
    booktitle = "INTERSPEECH",
    year = "2017",
}
"""

_DESCRIPTION = """\
VoxCeleb is an audio-visual dataset consisting of short clips of human speech, extracted from interview videos uploaded to YouTube
"""

_URL = "https://mm.kaist.ac.kr/datasets/voxceleb"
_REQ_URL = "https://cn01.mmai.io/keyreq/voxceleb"

_URLS = {
    "video": {
        "placeholder": "https://cn01.mmai.io/download/voxceleb?file=vox2_dev_mp4",
        "dev": (
            "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox2_dev_mp4_partaa",
            "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox2_dev_mp4_partab",
            "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox2_dev_mp4_partac",
            "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox2_dev_mp4_partad",
            "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox2_dev_mp4_partae",
            "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox2_dev_mp4_partaf",
            "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox2_dev_mp4_partag",
            "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox2_dev_mp4_partah",
            "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox2_dev_mp4_partai",
        ),
        "test": "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox2_test_mp4.zip",
    },
    "audio1": {
        "placeholder": "https://cn01.mmai.io/download/voxceleb?file=vox1_dev_wav",
        "dev": (
            "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox1_dev_wav_partaa",
            # "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox1_dev_wav_partab",
            # "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox1_dev_wav_partac",
            # "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox1_dev_wav_partad",
        ),
        "test": "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox1_test_wav.zip",
    },
    "audio2": {
        "placeholder": "https://cn01.mmai.io/download/voxceleb?file=vox2_dev_aac",
        "dev": (
            "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox2_dev_aac_partaa",
            "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox2_dev_aac_partab",
            "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox2_dev_aac_partac",
            "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox2_dev_aac_partad",
            "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox2_dev_aac_partae",
            "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox2_dev_aac_partaf",
            "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox2_dev_aac_partag",
            "https://cn01.mmai.io/download/voxceleb?key={key}&file=vox2_dev_aac_partah",
        ),
        "test": "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_test_aac.zip",
    },
}

_NO_AUTH_URLS = {
    "video": {
        "placeholder": "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_mp4",
        "dev": (
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_mp4_partaa",
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_mp4_partab",
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_mp4_partac",
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_mp4_partad",
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_mp4_partae",
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_mp4_partaf",
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_mp4_partag",
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_mp4_partah",
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_mp4_partai",
        ),
        "test": "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_test_mp4.zip",
    },
    "audio1": {
        "placeholder": "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox1/vox1_dev_wav",
        "dev": (
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox1/vox1_dev_wav_partaa",
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox1/vox1_dev_wav_partab",
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox1/vox1_dev_wav_partac",
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox1/vox1_dev_wav_partad",
        ),
        "test": "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox1/vox1_test_wav.zip",
    },
    "audio2": {
        "placeholder": "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_aac",
        "dev": (
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_aac_partaa",
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_aac_partab",
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_aac_partac",
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_aac_partad",
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_aac_partae",
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_aac_partaf",
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_aac_partag",
            "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_dev_aac_partah",
        ),
        "test": "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_test_aac.zip",
    },
}

_DATASET_IDS = {"video": "vox2", "audio1": "vox1", "audio2": "vox2"}

_PLACEHOLDER_MAPS = dict(
    value
    for urls in (*_URLS.values(), *_NO_AUTH_URLS.values())
    for value in ((urls["placeholder"], urls["dev"]), (urls["test"], (urls["test"],)))
)

def _mp_download(
    url,
    tmp_path,
    cred_key,
    resume_pos,
    length,
    queue,
):
    if length == resume_pos:
        return
    with open(tmp_path, "ab" if resume_pos else "wb") as tmp:
        headers = {}
        if resume_pos != 0:
            headers["Range"] = f"bytes={resume_pos}-"
        with catch_warnings():
            filterwarnings("ignore", category=InsecureRequestWarning)
            response = requests.get(
                url.format(key=cred_key), headers=headers, verify=False, stream=True
            )
        if response.status_code >= 200 and response.status_code < 300:
            for chunk in response.iter_content(chunk_size=65536):
                queue.put(len(chunk))
                tmp.write(chunk)
        else:
            raise ConnectionError("failed to fetch dataset")


class VoxCeleb(datasets.GeneratorBasedBuilder):
    """VoxCeleb is an unlabled dataset consisting of short clips of human speech from interviews on YouTube"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="video", version=VERSION, description="Video clips of human speech"
        ),
        datasets.BuilderConfig(
            name="audio", version=VERSION, description="Audio clips of human speech"
        ),
        datasets.BuilderConfig(
            name="audio1",
            version=datasets.Version("1.0.0"),
            description="Audio clips of human speech from VoxCeleb1",
        ),
        datasets.BuilderConfig(
            name="audio2",
            version=datasets.Version("2.0.0"),
            description="Audio clips of human speech from VoxCeleb2",
        ),
    ]

    def _info(self):
        features = {
            "file": datasets.Value("string"),
            "file_format": datasets.Value("string"),
            "dataset_id": datasets.Value("string"),
            "speaker_id": datasets.Value("string"),
            "speaker_gender": datasets.Value("string"),
            "video_id": datasets.Value("string"),
            "clip_index": datasets.Value("int32"),
        }
        if self.config.name == "audio1":
            features["speaker_name"] = datasets.Value("string")
            features["speaker_nationality"] = datasets.Value("string")
        if self.config.name.startswith("audio"):
            features["audio"] = datasets.Audio(sampling_rate=16000)

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            homepage=_URL,
            supervised_keys=datasets.info.SupervisedKeysData("file", "speaker_id"),
            features=datasets.Features(features),
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        if dl_manager.is_streaming:
            raise TypeError("Streaming is not supported for VoxCeleb")
        targets = (
            ["audio1", "audio2"] if self.config.name == "audio" else [self.config.name]
        )
        cred_key = os.environ.get("HUGGING_FACE_VOX_CELEB_KEY")
        hf_dir = os.getenv(
            "HF_HOME",
            os.path.join(
                os.getenv("XDG_CACHE_HOME", os.path.join(os.path.expanduser("~"), ".cache")),
                "huggingface"
            )
        )
        creds_path = Path(hf_dir) / f"voxceleb_{self.VERSION}_credentials"
        all_urls = _URLS

        if cred_key is None:
            if creds_path.exists():
                with open(creds_path, "r") as creds:
                    cred_key = json.load(creds)
            else:
                print(
                    "You need a key to access VoxCeleb directly.",
                    f"Fill out the form ({_REQ_URL}) and paste in any of the download links you receive in your email.",
                    "Alternatively, enter an empty string to use a third-party proxy by https://huggingface.co/ProgramComputer."
                )
                cred_url = getpass("Paste any VoxCeleb download URL here (leave blank for proxy): ")
                if cred_url != "":
                    cred_url_parsed = urlparse(cred_url)
                    if cred_url_parsed.scheme != 'https' or cred_url_parsed.hostname != 'cn01.mmai.io' or cred_url_parsed.path != '/download/voxceleb':
                        raise ValueError("couldn't parse as VoxCeleb download URL")
                    cred_url_query = parse_qs(cred_url_parsed.query)
                    if 'key' not in cred_url_query or len(cred_url_query['key']) != 1:
                        raise ValueError("couldn't find key in URL")
                    cred_key = cred_url_query['key'][0]

        if cred_key is None:
            all_urls = _NO_AUTH_URLS

        saved_credentials = False

        def save_credentials():
            nonlocal saved_credentials, cred_key, creds_path
            if not saved_credentials:
                creds_path.parent.mkdir(exist_ok=True)
                with open(creds_path, "w") as creds:
                    json.dump(cred_key, creds)
                saved_credentials = True

        def download_custom(placeholder_url, path):
            nonlocal dl_manager, cred_key
            sources = _PLACEHOLDER_MAPS[placeholder_url]
            tmp_paths = []
            lengths = []
            start_positions = []
            for url in sources:
                with catch_warnings():
                    filterwarnings("ignore", category=InsecureRequestWarning)
                    head = requests.get(url.format(key=cred_key), verify=False, timeout=5, stream=True)
                try:
                    if head.status_code == 401:
                        raise ValueError("failed to authenticate with VoxCeleb host")
                    if head.status_code < 200 or head.status_code >= 300:
                        raise ValueError("failed to fetch dataset")
                    save_credentials()
                    content_length = head.headers.get("Content-Length")
                    if content_length is None:
                        raise ValueError("expected non-empty Content-Length")
                    content_length = int(content_length)
                finally:
                    head.close()
                tmp_path = Path(path + "." + sha256(url.encode("utf-8")).hexdigest())
                tmp_paths.append(tmp_path)
                lengths.append(content_length)
                start_positions.append(
                    tmp_path.stat().st_size
                    if tmp_path.exists() and dl_manager.download_config.resume_download
                    else 0
                )

            def progress(q, cur, total):
                with datasets.utils.logging.tqdm(
                    unit="B",
                    unit_scale=True,
                    total=total,
                    initial=cur,
                    desc="Downloading",
                    disable=not datasets.utils.logging.is_progress_bar_enabled(),
                ) as progress:
                    while cur < total:
                        try:
                            added = q.get(timeout=1)
                            progress.update(added)
                            cur += added
                        except:
                            continue

            manager = Manager()
            q = manager.Queue()
            with Pool(len(sources)) as pool:
                proc = Process(
                    target=progress,
                    args=(q, sum(start_positions), sum(lengths)),
                    daemon=True,
                )
                proc.start()
                pool.starmap(
                    _mp_download,
                    zip(
                        sources,
                        tmp_paths,
                        repeat(cred_key),
                        start_positions,
                        lengths,
                        repeat(q),
                    ),
                )
                pool.close()
                proc.join()
            with open(path, "wb") as out:
                for tmp_path in tmp_paths:
                    with open(tmp_path, "rb") as tmp:
                        copyfileobj(tmp, out)
                    tmp_path.unlink()

        metadata = dl_manager.download(
            dict(
                (
                    target,
                    f"https://mm.kaist.ac.kr/datasets/voxceleb/meta/{_DATASET_IDS[target]}_meta.csv",
                )
                for target in targets
            )
        )

        mapped_paths = dl_manager.extract(
            dl_manager.download_custom(
                dict(
                    (
                        placeholder_key,
                        dict(
                            (target, all_urls[target][placeholder_key])
                            for target in targets
                        ),
                    )
                    for placeholder_key in ("placeholder", "test")
                ),
                download_custom,
            )
        )

        return [
            datasets.SplitGenerator(
                name="train",
                gen_kwargs={
                    "paths": mapped_paths["placeholder"],
                    "meta_paths": metadata,
                },
            ),
            datasets.SplitGenerator(
                name="test",
                gen_kwargs={
                    "paths": mapped_paths["test"],
                    "meta_paths": metadata,
                },
            ),
        ]

    def _generate_examples(self, paths, meta_paths):
        key = 0
        for conf in paths:
            dataset_id = "vox1" if conf == "audio1" else "vox2"
            meta = pd.read_csv(
                meta_paths[conf],
                sep="\t" if conf == "audio1" else " ,",
                index_col=0,
                engine="python",
            )
            dataset_path = next(Path(paths[conf]).iterdir())
            dataset_format = dataset_path.name
            for speaker_path in dataset_path.iterdir():
                speaker = speaker_path.name
                speaker_info = meta.loc[speaker]
                for video in speaker_path.iterdir():
                    video_id = video.name
                    for clip in video.iterdir():
                        clip_index = int(clip.stem)
                        info = {
                            "file": str(clip),
                            "file_format": dataset_format,
                            "dataset_id": dataset_id,
                            "speaker_id": speaker,
                            "speaker_gender": speaker_info["Gender"],
                            "video_id": video_id,
                            "clip_index": clip_index,
                        }
                        if dataset_id == "vox1":
                            info["speaker_name"] = speaker_info["VGGFace1 ID"]
                            info["speaker_nationality"] = speaker_info["Nationality"]
                        if conf.startswith("audio"):
                            info["audio"] = info["file"]
                        yield key, info
                        key += 1
