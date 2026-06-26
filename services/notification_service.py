from services.dashboard_service import (
    get_artwork_kpis
)


def get_notifications():

    kpis = get_artwork_kpis()


    notifications = []


    if kpis["Draft"] > 0:

        notifications.append(
            {
                "type": "warning",
                "title": "Artwork waiting for review",
                "count": kpis["Draft"],
                "page": "Artwork Review"
            }
        )


    if kpis["Approved"] > 0:

        notifications.append(
            {
                "type": "success",
                "title": "Artwork waiting for release",
                "count": kpis["Approved"],
                "page": "Artwork Release"
            }
        )


    if kpis["Rejected"] > 0:

        notifications.append(
            {
                "type": "error",
                "title": "Rejected artwork requires action",
                "count": kpis["Rejected"],
                "page": "Artwork Review"
            }
        )


    return notifications