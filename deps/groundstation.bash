groundstation_dev() {
    requires "pip_packages_installed"
    process
}

virtualenv_exists() {
    #requires "virtualenv installed"
    function is_met() {
        test -d env
    }
    function meet() {
        virtualenv env
    }
    process
}

pip_packages_installed() {
    requires "virtualenv_exists"
    function is_met() {
        (
            . env/bin/activate
            # Nasty
            for i in pygit2 google.protobuf; do
                python -c "import $i" || exit 1
            done
        )
    }
    function meet() {
        (
            . env/bin/activate
            pip install -r requirements.txt
        )
    }
    process
}
