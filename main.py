from links import read_list_of_links, gen_dict_of_links
from mhtmls import gen_only_home_mhtmls


def print_finished():
    print("** Finished **")


def main():
    list_of_links = read_list_of_links('links.txt')
    dict_of_links = gen_dict_of_links(list_of_links, "lists_of_links")
    gen_only_home_mhtmls(list_of_links, "mhtmls")
    print_finished()


if __name__ == '__main__':
    main()
