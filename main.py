from links import read_list_of_links, gen_dict_of_links
from mhtmls import gen_mhtmls, gen_only_home_mhtmls


def print_finished():
    print("\n** Finished **\n")


def main():
    list_of_links = read_list_of_links(links_path='links.txt')
    dict_of_links, failed_links = gen_dict_of_links(list_of_links, output_dir_name="list_of_links")
    gen_only_home_mhtmls(list_of_links, failed_links, output_dir_name="mhtmls")
    gen_mhtmls(list_of_links, dict_of_links, failed_links, output_dir_name="mhtmls")
    print_finished()


if __name__ == '__main__':
    main()
