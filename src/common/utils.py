def get_or_create(db, model, **kwargs):
    record = db.session.query(model).filter_by(**kwargs).first()
    if record:
        return record
    else:
        record = model(**kwargs)
        db.session.add(record)
        db.session.commit()
        return record
