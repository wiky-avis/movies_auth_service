def get_pagination(paginator, data):
    return {
        "page": paginator.page,
        "pages": paginator.pages,
        "total_count": paginator.total,
        "prev_page": paginator.prev_num,
        "next_page": paginator.next_num,
        "has_next": paginator.has_next,
        "has_prev": paginator.has_prev,
        "results": data,
    }
