nuitka \
--remove-output \
--onefile \
--onefile-cache-mode=cached \
--onefile-tempdir-spec="{TEMP}/RSEMI" \
--linux-icon=res/init.ico \
--output-filename=RS-EMI \
--product-name=RS-EMI \
--product-version=1.0 \
--enable-plugin=pyside6 \
--lto=yes \
"RSEMI.py"
