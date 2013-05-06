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

python_dev_installed() {
    install_package python-dev
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

libgit2_from_git() {
    requires "virtualenv_exists"

    function is_met() {
        echo "main() { return 0; }" | gcc -x c /dev/stdin -lgit2 -o /dev/null
    }
    function meet() {
        git clone git://github.com/libgit2/libgit2.git env/src/libgit2
        (
          cd env/src/libgit2
          ./autogen.sh
          make
          $__babashka_sudo make install
        )
    }
}

virtualenv_exists() {
    requires "virtualenv_installed"
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
    requires "python_dev_installed"
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

virtualenv_installed() {
    function is_met() {
        which virtualenv
    }
    function meet() {
        case `uname -s` in
            Linux)
                # TODO Non debian derivatives
                $__babashka_sudo aptitude install python-virtualenv
                ;;
            Darwin)
                pip install virtualenv
                ;;
        esac
    }
    process
}
