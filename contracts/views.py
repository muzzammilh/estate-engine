def get_filtered_queryset(queryset, request):
    property_id = request.GET.get('property')
    unit_id = request.GET.get('unit')

    if property_id:
        queryset = queryset.filter(unit__property_id=property_id)
    if unit_id:
        queryset = queryset.filter(unit_id=unit_id)

    return queryset
