{
  "cells": [
    {
      "cell_type": "markdown",
      "id": "57ced40c",
      "metadata": {
        "id": "57ced40c"
      },
      "source": [
        "# F1 Tyre Degradation and Strategy Simulation\n",
        "\n",
        "This notebook presents a simplified modelling approach to tyre degradation in Formula 1\n",
        "and evaluates pit-stop strategies based on degradation behaviour.\n",
        "\n",
        "The objective is to study how degradation trends influence optimal pit windows under\n",
        "controlled assumptions."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "id": "CG2_DBstpGCK",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "CG2_DBstpGCK",
        "outputId": "05034b75-b477-464f-f3ee-40f13aaa34b9"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Cloning into 'f1-tyre-strategy-colab'...\n",
            "remote: Enumerating objects: 43, done.\u001b[K\n",
            "remote: Counting objects: 100% (43/43), done.\u001b[K\n",
            "remote: Compressing objects: 100% (28/28), done.\u001b[K\n",
            "remote: Total 43 (delta 17), reused 34 (delta 9), pack-reused 0 (from 0)\u001b[K\n",
            "Receiving objects: 100% (43/43), 64.33 KiB | 548.00 KiB/s, done.\n",
            "Resolving deltas: 100% (17/17), done.\n",
            "/content/f1-tyre-strategy-colab\n",
            "Requirement already satisfied: attrs==25.4.0 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 1)) (25.4.0)\n",
            "Requirement already satisfied: cattrs==25.3.0 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 2)) (25.3.0)\n",
            "Requirement already satisfied: certifi==2026.1.4 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 3)) (2026.1.4)\n",
            "Requirement already satisfied: cffi==2.0.0 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 4)) (2.0.0)\n",
            "Requirement already satisfied: charset-normalizer==3.4.4 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 5)) (3.4.4)\n",
            "Requirement already satisfied: contourpy==1.3.3 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 6)) (1.3.3)\n",
            "Requirement already satisfied: cryptography==46.0.4 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 7)) (46.0.4)\n",
            "Requirement already satisfied: cycler==0.12.1 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 8)) (0.12.1)\n",
            "Requirement already satisfied: fastf1==3.7.0 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 9)) (3.7.0)\n",
            "Requirement already satisfied: fonttools==4.61.1 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 10)) (4.61.1)\n",
            "Requirement already satisfied: idna==3.11 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 11)) (3.11)\n",
            "Requirement already satisfied: joblib==1.5.3 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 12)) (1.5.3)\n",
            "Requirement already satisfied: kiwisolver==1.4.9 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 13)) (1.4.9)\n",
            "Requirement already satisfied: matplotlib==3.10.8 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 14)) (3.10.8)\n",
            "Requirement already satisfied: msgpack==1.0.2 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 15)) (1.0.2)\n",
            "Requirement already satisfied: numpy==2.4.2 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 16)) (2.4.2)\n",
            "Requirement already satisfied: packaging==26.0 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 17)) (26.0)\n",
            "Requirement already satisfied: pandas==2.3.3 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 18)) (2.3.3)\n",
            "Requirement already satisfied: pillow==12.1.0 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 19)) (12.1.0)\n",
            "Requirement already satisfied: platformdirs==4.5.1 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 20)) (4.5.1)\n",
            "Requirement already satisfied: pycparser==3.0 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 21)) (3.0)\n",
            "Requirement already satisfied: PyJWT==2.11.0 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 22)) (2.11.0)\n",
            "Requirement already satisfied: pyparsing==3.3.2 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 23)) (3.3.2)\n",
            "Requirement already satisfied: python-dateutil==2.9.0.post0 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 24)) (2.9.0.post0)\n",
            "Requirement already satisfied: pytz==2025.2 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 25)) (2025.2)\n",
            "Requirement already satisfied: RapidFuzz==3.14.3 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 26)) (3.14.3)\n",
            "Requirement already satisfied: requests==2.32.5 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 27)) (2.32.5)\n",
            "Requirement already satisfied: requests-cache==1.2.1 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 28)) (1.2.1)\n",
            "Requirement already satisfied: scikit-learn==1.8.0 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 29)) (1.8.0)\n",
            "Requirement already satisfied: scipy==1.17.0 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 30)) (1.17.0)\n",
            "Requirement already satisfied: seaborn==0.13.2 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 31)) (0.13.2)\n",
            "Requirement already satisfied: signalrcore==0.9.71 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 32)) (0.9.71)\n",
            "Requirement already satisfied: six==1.17.0 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 33)) (1.17.0)\n",
            "Requirement already satisfied: threadpoolctl==3.6.0 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 34)) (3.6.0)\n",
            "Requirement already satisfied: timple==0.1.8 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 35)) (0.1.8)\n",
            "Requirement already satisfied: tqdm==4.67.2 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 36)) (4.67.2)\n",
            "Requirement already satisfied: typing_extensions==4.15.0 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 37)) (4.15.0)\n",
            "Requirement already satisfied: tzdata==2025.3 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 38)) (2025.3)\n",
            "Requirement already satisfied: url-normalize==2.2.1 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 39)) (2.2.1)\n",
            "Requirement already satisfied: urllib3==2.6.3 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 40)) (2.6.3)\n",
            "Requirement already satisfied: websockets==16.0 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 41)) (16.0)\n"
          ]
        }
      ],
      "source": [
        "!rm -rf f1-tyre-strategy-colab\n",
        "!git clone https://github.com/Sneha73685/f1-tyre-strategy-colab.git\n",
        "%cd f1-tyre-strategy-colab\n",
        "!pip install -r requirements.txt"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 3,
      "id": "0903f2d7",
      "metadata": {
        "id": "0903f2d7"
      },
      "outputs": [],
      "source": [
        "import sys\n",
        "sys.path.append(\"src\")"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 4,
      "id": "ce54c5d9",
      "metadata": {
        "id": "ce54c5d9"
      },
      "outputs": [],
      "source": [
        "import numpy as np\n",
        "import pandas as pd\n",
        "import matplotlib.pyplot as plt\n",
        "\n",
        "from data_loader import load_race_data\n",
        "race_data = load_race_data(\"data/processed/race_data.csv\")\n",
        "race_data.head()\n",
        "\n",
        "from degradation import TyreDegradationModel\n",
        "\n",
        "model = TyreDegradationModel(alpha=0.03)\n",
        "model.fit(race_data)\n",
        "from strategy import simulate_strategy"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "\n",
        "tyre_life = np.arange(1, 31)\n",
        "curve = model.predict(tyre_life)\n",
        "\n",
        "plt.figure()\n",
        "plt.plot(tyre_life, curve)\n",
        "plt.xlabel(\"Tyre Life (laps)\")\n",
        "plt.ylabel(\"Relative Performance\")\n",
        "plt.title(\"Tyre Degradation vs Tyre Life\")\n",
        "plt.show()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 269
        },
        "id": "sbSfMc6JtZlf",
        "outputId": "dd8fe93f-7fd1-4198-a5db-f6739b8f5115"
      },
      "id": "sbSfMc6JtZlf",
      "execution_count": 5,
      "outputs": [
        {
          "output_type": "error",
          "ename": "TypeError",
          "evalue": "TyreDegradationModel.predict() takes 1 positional argument but 2 were given",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mTypeError\u001b[0m                                 Traceback (most recent call last)",
            "\u001b[0;32m/tmp/ipython-input-1595488875.py\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0mtyre_life\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mnp\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0marange\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;36m1\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;36m31\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 5\u001b[0;31m \u001b[0mcurve\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mmodel\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mpredict\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mtyre_life\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      6\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      7\u001b[0m \u001b[0mplt\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mfigure\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mTypeError\u001b[0m: TyreDegradationModel.predict() takes 1 positional argument but 2 were given"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "id": "02963b59",
      "metadata": {
        "id": "02963b59"
      },
      "source": [
        "## Data Description\n",
        "\n",
        "The analysis operates on preprocessed race-level data stored locally for reproducibility.\n",
        "Each row represents lap-level information used to simulate tyre degradation behaviour."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "id": "894e19ab",
      "metadata": {
        "id": "894e19ab"
      },
      "outputs": [],
      "source": [
        "race_data = load_race_data(\"data/processed/race_data.csv\")\n",
        "race_data.head()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "id": "1a454dfa",
      "metadata": {
        "id": "1a454dfa"
      },
      "outputs": [],
      "source": [
        "model = TyreDegradationModel(alpha=0.03)\n",
        "model.fit(race_data)\n",
        "\n",
        "degradation_curve = model.predict()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "id": "d0d1a677",
      "metadata": {
        "id": "d0d1a677"
      },
      "outputs": [],
      "source": [
        "plt.figure()\n",
        "plt.plot(degradation_curve)\n",
        "plt.xlabel(\"Lap\")\n",
        "plt.ylabel(\"Relative Performance\")\n",
        "plt.title(\"Tyre Degradation Curve Over a Stint\")\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "id": "10043e4b",
      "metadata": {
        "id": "10043e4b"
      },
      "outputs": [],
      "source": [
        "total_laps = 70\n",
        "pit_window = (15, 40)\n",
        "\n",
        "results = simulate_strategy(\n",
        "    degradation_model=model,\n",
        "    total_laps=total_laps,\n",
        "    pit_window=pit_window\n",
        ")"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "id": "16161660",
      "metadata": {
        "id": "16161660"
      },
      "outputs": [],
      "source": [
        "results_df = pd.DataFrame(\n",
        "    results,\n",
        "    columns=[\"Pit Lap\", \"Total Degradation Cost\"]\n",
        ")\n",
        "\n",
        "results_df.head()\n",
        "\n",
        "plt.figure()\n",
        "plt.plot(results_df[\"Pit Lap\"], results_df[\"Total Degradation Cost\"])\n",
        "plt.xlabel(\"Pit Stop Lap\")\n",
        "plt.ylabel(\"Total Degradation Cost\")\n",
        "plt.title(\"Pit Stop Strategy Evaluation\")\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from strategy import simulate_strategy\n",
        "\n",
        "results = simulate_strategy(\n",
        "    degradation_model=model,\n",
        "    total_laps=70,\n",
        "    pit_window=(15, 40)\n",
        ")\n",
        "\n",
        "import pandas as pd\n",
        "results_df = pd.DataFrame(results, columns=[\"Pit Lap\", \"Total Degradation Cost\"])\n",
        "results_df.head()"
      ],
      "metadata": {
        "id": "gHPujR-Jthsg"
      },
      "id": "gHPujR-Jthsg",
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "plt.figure()\n",
        "plt.plot(results_df[\"Pit Lap\"], results_df[\"Total Degradation Cost\"])\n",
        "plt.xlabel(\"Pit Stop Lap\")\n",
        "plt.ylabel(\"Total Degradation Cost\")\n",
        "plt.title(\"One-Stop Pit Strategy Evaluation\")\n",
        "plt.show()"
      ],
      "metadata": {
        "id": "ULknj8H5tivB"
      },
      "id": "ULknj8H5tivB",
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "id": "c32fcbe8",
      "metadata": {
        "id": "c32fcbe8"
      },
      "source": [
        "## Observations\n",
        "\n",
        "- Early pit stops reduce late-stint degradation but shorten the first stint.\n",
        "- Late pit stops increase degradation accumulation in the second stint.\n",
        "- A mid-range pit window provides a balance between stint length and degradation cost."
      ]
    },
    {
      "cell_type": "markdown",
      "id": "9331d7cf",
      "metadata": {
        "id": "9331d7cf"
      },
      "source": [
        "## Assumptions and Limitations\n",
        "\n",
        "- Tyre degradation is modelled using a simplified exponential decay function.\n",
        "- External race factors such as traffic, safety cars, weather, and tyre compounds\n",
        "  are not considered.\n",
        "- The objective is to demonstrate modelling and strategy logic rather than\n",
        "  exact race prediction."
      ]
    },
    {
      "cell_type": "markdown",
      "id": "d50cc81c",
      "metadata": {
        "id": "d50cc81c"
      },
      "source": [
        "## Data Source Note\n",
        "\n",
        "Raw Formula 1 telemetry can be accessed using the FastF1 Python API.\n",
        "For reproducibility, this notebook operates on preprocessed datasets."
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "race_data.columns"
      ],
      "metadata": {
        "id": "Y69Udst9t3ce"
      },
      "id": "Y69Udst9t3ce",
      "execution_count": null,
      "outputs": []
    }
  ],
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "display_name": "venv",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "name": "python",
      "version": "3.12.12"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 5
}