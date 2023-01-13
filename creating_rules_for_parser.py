import pickle

def rules_mangaclash(path_dict):
    # open rules dict
    with open(path_dict, 'rb') as handle:
        rule_dict = pickle.load(handle)

    # creating rules
    chapters_block = 'li'
    chapters_class = 'wp-manga-chapter'

    chapter_link_block = 'a'
    chapter_link_attrib = 'href'

    images_block = 'img'
    images_class = 'wp-manga-chapter-img'
    image_link_attrib = 'data-src'

    # filling rules dict
    rule_dict['mangaclash'] = {}
    rule_dict.get('mangaclash').update({'chapters_block': chapters_block})
    rule_dict.get('mangaclash').update({'chapters_class': chapters_class})
    rule_dict.get('mangaclash').update({'chapter_link_block': chapter_link_block})
    rule_dict.get('mangaclash').update({'chapter_link_attrib': chapter_link_attrib})
    rule_dict.get('mangaclash').update({'images_block': images_block})
    rule_dict.get('mangaclash').update({'images_class': images_class})
    rule_dict.get('mangaclash').update({'image_link_attrib': image_link_attrib})
    with open(path_dict, 'wb') as handle:
            pickle.dump(rule_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    rules_mangaclash('test.pickle')