def restructureCSQAChoices(choices):
    string_list = []
    for i in range(len(choices)):
        string = ""
        for i in range(5):
            string += f'{choices["label"][i]}) {choices["text"][i]}\n'
        string_list.append(string)
    return string_list
