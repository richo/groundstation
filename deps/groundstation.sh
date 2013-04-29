groundstation_dev() {
    requires "libgit2_dev"
    requires "pip_packages_installed"
    process
}

build_essential_installed() {
    # TODO osx
    install_package build-essential
    process
}

libgit2_dev() {
    requires "build_essential_installed"

    case `uname -s` in
        Darwin)
            function is_met() {
                echo "main() { return 0; }" | gcc -x c /dev/stdin -lgit2 -o /dev/null
            }
            function meet {
                brew install --HEAD libgit2
            }
            process;;
        *)
            requires "libgit2_from_git";;
    esac
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
