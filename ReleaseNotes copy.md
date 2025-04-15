# Installation Instructions for `ddm_engine`

You can install `ddm_engine` in two ways: **Manual** or **Automatic**.

---

## 🔧 Manual Installation

> 💡 It is **strongly recommended** to use a separate Python virtual environment.

### Steps:

1. **Activate your virtual environment**

2. **Place the `Wheelhouse` folder** into a specific directory of your choice.

3. **Run the installation command** from either `CMD` or `PowerShell`:

```bash
pip install ddm_engine --no-index -f Wheelhouse
```

### Upgrading an Existing Installation

To force an upgrade of `ddm_engine`:

```bash
pip install --upgrade --force-reinstall ddm_engine --no-index -f Wheelhouse
```

### Additional NLP Models

After installation, you must also install the following language models manually (located in the same `Wheelhouse` folder):

- `en_core_web_sm`
- `fr_core_news_sm`
- `nl_core_news_sm`

---

## ⚙️ Automatic Installation

1. **Place the following files into a specific directory:**
   - `dynamic_data_masking_install.ps1`
   - `Wheelhouse` folder

2. **Run the PowerShell script with the required parameters:**

```powershell
.\dynamic_data_masking_install.ps1 -TargetPath "<path_to_virtual_env>" -VenvName "<your_venv_name>"
```

### What this does:
- Activates the specified virtual environment
- Installs the contents of the `Wheelhouse`
- Automatically installs all required dependencies and the necessary NLP NER models

---

Happy masking! 😎

