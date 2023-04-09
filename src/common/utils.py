import logging

from email_validator import EmailNotValidError, validate_email


logger = logging.getLogger(__name__)


def get_or_create(db, model, **kwargs):
    record = db.session.query(model).filter_by(**kwargs).first()
    if record:
        return record
    else:
        record = model(**kwargs)
        db.session.add(record)
        db.session.commit()
        return record


def get_valid_email(email):
    try:
        validation = validate_email(email, check_deliverability=True)
    except EmailNotValidError:
        logger.error("Email is not valid: s%", email, exc_info=True)
        return None
    return validation.email
