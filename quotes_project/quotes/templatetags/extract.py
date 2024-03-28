# from bson import ObjectId as Obd
from django import template


# from ..utils import get_mongodb
from ..models import Author

GREEN = "\033[92m"
RESET = "\033[0m"

register = template.Library()


# def get_author(id_):
#     db = get_mongodb()
#     author = db.authors.find_one({"_id": Obd(id_)})
#     return author["fullname"]
#
#
# register.filter("author", get_author)


def get_author(id_):
    try:
        author = Author.objects.get(pk=id_)
        return author.fullname
    except Author.DoesNotExist:
        return f"{GREEN}Author does not exist!{RESET}"


register.filter("author", get_author)
