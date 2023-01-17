


def endResult(student, numberOfCredit, semester):

    if numberOfCredit >= 11:
        if semester == "اول":
            semester = "دوم"
        elif semester == "دوم":
            semester = "سوم"
        elif semester == "سوم":
            semester = "چهارم"
        elif semester == "چهارم":
            semester = "پنجم"
        elif semester == "پنجم":
            semester = "ششم"

        elif semester == "ششم":
            semester = "هفتم"

        elif semester == "هفتم":
            semester = "هشتم"

    return student

