import logging

logger = logging.getLogger(__name__)

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import HTTPException
from flask_pydantic import validate
from api.base.base_schemas import BaseResponse
from middlewares.authentication import get_user_id_from_access_token

from .schemas import (
    CreateNoteRequest,
    CreateNoteResponse,
    ReadNoteResponse,
    ReadAllNoteParamRequest,
    ReadAllNoteResponse,
    UpdateNoteRequest,
    UpdateNoteResponse,
    DeleteNoteResponse
)
from .use_cases import CreateNote, ReadAllNote, ReadNote, UpdateNote, DeleteNote

router = Blueprint("notes", __name__, url_prefix='/api/v1/notes')

@router.route("/add", methods=['POST'])
@validate()
def create(
    body: CreateNoteRequest,
) -> CreateNoteResponse:
    try:
        user_id = get_user_id_from_access_token(request)
        resp_data = CreateNote().execute(
            request=body,
            user_id=user_id
        )

        return jsonify(CreateNoteResponse(
            status="success",
            message="success add new note",
            data=resp_data.dict(),
        ).__dict__), 200
    except HTTPException as ex:
        return jsonify(CreateNoteResponse(
            status="error",
            message=ex.description,
            data=None
        ).__dict__), ex.code
    except Exception as e:
        message = "failed to add new note"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return jsonify(CreateNoteResponse(
            status="error",
            message=message,
            data=None
        ).__dict__), 500


@router.route("/", methods=["GET"])
@validate()
def read_all(
    query: ReadAllNoteParamRequest,
):
    try:
        user_id = get_user_id_from_access_token(request)
        filter_by_user_id = query.filter_by_user_id

        read_all = ReadAllNote()
        resp_data = read_all.execute(
            user_id=user_id,
            page_params=query,
            filter_by_user_id=filter_by_user_id,
        )

        return jsonify(ReadAllNoteResponse(
            status="success",
            message="success read notes",
            data={"records": resp_data[0], "meta": resp_data[1].__dict__},
        ).__dict__), 200
    except HTTPException as ex:
        return jsonify(ReadAllNoteResponse(
            status="error",
            message=ex.description,
            data=None
        ).__dict__), ex.code
    except Exception as e:
        message = "failed to read notes"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return jsonify(ReadAllNoteResponse(
            status="error",
            message=message,
            data=None
        ).__dict__), 500


# @router.route("/<note_id>", methods=["GET"])
# @validate()
# def read(
#     note_id: int
# ):
#     try:
#         get_user_id_from_access_token(request)

#         read_note = ReadNote()
#         resp_data = read_note.execute(note_id=note_id)

#         return jsonify(ReadNoteResponse(
#             status="success",
#             message="success read user",
#             data=resp_data.__dict__,
#         ).__dict__), 200
#     except HTTPException as ex:
#         return jsonify(ReadNoteResponse(
#             status="error",
#             message=ex.description,
#             data=None
#         ).__dict__), ex.code
#     except Exception as e:
#         message = "failed to read user"
#         if hasattr(e, "message"):
#             message = e.message
#         elif hasattr(e, "detail"):
#             message = e.detail

#         return jsonify(ReadNoteResponse(
#             status="error",
#             message=message,
#             data=None
#         ).__dict__), 500

@router.route("/<note_id>", methods=["GET"])
@validate()
def read(
    note_id: int
):
    try:
        user_id = get_user_id_from_access_token(request)

        read_note = ReadNote()
        resp_data = read_note.execute(note_id=note_id, user_id=user_id)

        return jsonify(ReadNoteResponse(
            status="success",
            message="success read user",
            data=resp_data.__dict__,
        ).__dict__), 200
    except HTTPException as ex:
        return jsonify(ReadNoteResponse(
            status="error",
            message=ex.description,
            data=None
        ).__dict__), ex.code
    except Exception as e:
        message = "failed to read user"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return jsonify(ReadNoteResponse(
            status="error",
            message=message,
            data=None
        ).__dict__), 500

@router.route("/<note_id>", methods=["PUT"])
@validate()
def update(
    body: UpdateNoteRequest,note_id: int,
):
    try:
        token_user_id = get_user_id_from_access_token(request)

        update_note = UpdateNote()
        resp_data = update_note.execute(user_id=token_user_id,note_id=note_id, request=body)

        return jsonify(UpdateNoteResponse(
            status="success",
            message="success update user",
            data=resp_data.__dict__,
        ).__dict__), 200
    except HTTPException as ex:
        return jsonify(UpdateNoteResponse(
            status="error",
            message=ex.description,
            data=None
        ).__dict__), ex.code
    except Exception as e:
        message="failed to update user"
        if hasattr(e, 'message'):
            message = e.message
        elif hasattr(e, 'detail'):
            message = e.detail

        return jsonify(UpdateNoteResponse(
            status="error",
            message=message,
            data=None
        ).__dict__), 500

@router.route("/<note_id>", methods=["DELETE"])
@validate()
def delete(
    note_id: int,
):
    try:
        token_user_id = get_user_id_from_access_token(request)
        delete_note = DeleteNote()
        resp_data = delete_note.execute(user_id=token_user_id,note_id=note_id)

        return jsonify(DeleteNoteResponse(
            status="success",
            message="success delete user",
            data=resp_data.__dict__,
        ).__dict__), 200
    except HTTPException as ex:
        return jsonify(DeleteNoteResponse(
            status="error",
            message=ex.description,
            data=None
        ).__dict__), ex.code
    except Exception as e:
        message="failed to delete user"
        if hasattr(e, 'message'):
            message = e.message
        elif hasattr(e, 'detail'):
            message = e.detail

        return jsonify(DeleteNoteResponse(
            status="error",
            message=message,
            data=None
        ).__dict__), 500
