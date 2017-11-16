from language import LanguageApi
from storage import Storage
from time import sleep


def main():
    language = LanguageApi()
    storage = Storage()
    text_data = storage.get_text_data()
    for d in text_data:
        if storage.post_in_data(d['_id']):
            continue
        sleep(0.5)
        content = None
        if 'content' in d:
            content = d['content']
        language_result = language.get_result_for_storage(d['_id'], d['title'], content)
        # store results
        storage.add_temp_language_info(language_result)



if __name__ == '__main__':
    main()
