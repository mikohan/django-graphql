from graphene import String, Int, ID, Field, Interface, List


class ICategories(Interface):
    cat_id = ID(required=True)
    cat_name = String(required=True)
    cat_parent = ID(required=False)


class IEngines(Interface):
    engine_id = ID()
    engine_name = String()


class ICarModels(Interface):
    model_id = ID()
    model_name = String()


class IBrand(Interface):
    brand_id = ID()
    brand_name = String()
    brand_slug = String()


class IBucket(Interface):
    key = String()
    doc_count = Int()
