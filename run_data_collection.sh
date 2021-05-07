#!/bin/bash -e

options_msg="Please provide one of the following options:"
simple_desc="'simple' - to get list_of_links and HMTL files of only URLs in links.txt file"
all_desc="'all' - to get list_of_links and HTML files of URLs in links.txt file and URLs found on each webpage"
example_cmd="(e.g. $ bash run_data_collection.sh simple)"

build_venv() {
  printf "\nInstalling Python 3 dependencies ...\n"
  rm -rf ./venv
  python3 -m venv ./venv
  python3 -m pip -q install -r ./requirements.txt
}

# A script to run the Python 3 program.
#
# ----------------------------
# Example Usage:
# ('$' represents the CLI prompt)
#
# $ bash run_data_collection.sh simple  # To run the 'simple' version of the Python 3 program
# $ bash run_data_collection.sh all     # To run the 'all' version of the Python 3 program
#
# ----------------------------
#
# Exit codes:
# (1) - No argument provided.
# (2) - Invalid argument.
#
main() {
  if [ -n "$1" ]; then
    case "$1" in
    simple)
      build_venv
      printf "\nRunning 'simple' version of the Python 3 program ...\n"
      python3 -W ignore main.py simple
      ;;
    all)
      build_venv
      printf "\nRunning 'all' version of the Python 3 program ...\n"
      python3 -W ignore main.py all
      ;;
    *)
      printf "ERROR: Invalid argument. %s\n\t%s\n\t%s\n\t%s" "${options_msg}" "${simple_desc}" "${all_desc}" "${example_cmd}"
      exit 2
      ;;
    esac
  else
    printf "ERROR: No argument provided. %s\n\t%s\n\t%s\n\t%s" "${options_msg}" "${simple_desc}" "${all_desc}" "${example_cmd}"
    exit 1
  fi
}

main "$@"
