from language import LanguageApi
from storage import Storage


def main():
    language = LanguageApi()
    storage = Storage()
    text_data = storage.get_text_data()
    for d in text_data:
        language_result = language.get_result_for_storage(d._id, d.title, d.content)
        # store results
        storage.add_temp_language_info(language_result)



if __name__ == '__main__':
    main()
