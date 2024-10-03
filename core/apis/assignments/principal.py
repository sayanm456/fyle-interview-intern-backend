from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema, AssignmentSubmitSchema
principle_assignments_resources = Blueprint("principle_assignments_resources", __name__)


@principle_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    assignments = Assignment.get_assignments_by_grade(p.principle_id)
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)

@principle_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_of_teachers(p):
    """Returns list of teachers"""
    all_teachers = Assignment.filter(Assignment.teacher_id == p.principle_id).all()
    teachers_dump = AssignmentSubmitSchema().dump(all_teachers)
    return APIResponse.respond(data=teachers_dump)

@principle_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def regrade_assignment(p, incoming_payload):
    """Grade an assignment"""
    graded_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    
    regrade_assignment = Assignment.mark_grade(
        _id=graded_assignment_payload.id,
        grade=graded_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(regrade_assignment)
    return APIResponse.respond(data=graded_assignment_dump)


