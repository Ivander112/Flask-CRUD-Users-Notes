import datetime
import math

from werkzeug.exceptions import HTTPException

from sqlalchemy import func, select

from db import get_session
from api.base.base_schemas import PaginationMetaResponse, PaginationParams
from models.note import Note, NoteSchema
from .schemas import (
    CreateNoteRequest,
    UpdateNoteRequest
)

class CreateNote:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(self, request: CreateNoteRequest, user_id: int) -> NoteSchema:
        with self.session as session:
            existing_note = session.execute(
                select(Note).where(Note.title == request.title)
            ).scalars().first()
            
            if existing_note:
                exception = HTTPException(description=f"Note with title: {request.title} is already exist")
                exception.code = 400
                raise exception

            note = Note(
                title=request.title,
                content=request.content,
                created_by=user_id,
                created_at=datetime.datetime.utcnow()
            )

            session.add(note)
            session.flush()

            return NoteSchema.from_orm(note)

# class ReadNote:
#     def __init__(self) -> None:
#         self.session = get_session()

#     def execute(self, note_id: int) -> NoteSchema:
#         with self.session as session:
#             nt = session.execute(
#                 select(Note).where(
#                     (Note.note_id == note_id).__and__(Note.deleted_at == None)
#                 )
#             )
#             nt = nt.scalars().first()
#             if not nt:
#                 exception = HTTPException(description="note not found")
#                 exception.code = 404
#                 raise exception
#             return NoteSchema.from_orm(nt)
        

class ReadNote:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(self, note_id: int, user_id: int) -> NoteSchema:
        with self.session as session:
            nt = session.execute(
                select(Note).where(
                    (Note.note_id == note_id)
                    .__and__(Note.deleted_at == None)
                    .__and__(Note.created_by == user_id)
                )
            )
            nt = nt.scalars().first()
            if not nt:
                exception = HTTPException(description="note not found")
                exception.code = 404
                raise exception
            return NoteSchema.from_orm(nt)

class ReadAllNote:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(
            self,
            user_id: int,
            page_params: PaginationParams,
            filter_by_user_id: bool,
    ) -> (list[dict], PaginationMetaResponse):
        with self.session as session:
            if filter_by_user_id:
                total_item = session.execute(
                    select(func.count())
                    .select_from(Note)
                    .where((Note.deleted_at == None) & (Note.created_by == user_id))
                )
            else:
                # Jika tidak ada filter, hitung total item secara umum
                total_item = session.execute(
                    select(func.count())
                    .select_from(Note)
                    .where(Note.deleted_at == None)
                )

            # print("Total Item:", total_item)

            total_item = total_item.scalar()

            query = (
                select(Note)
                .where(Note.deleted_at.is_(None))
                .offset((page_params.page - 1) * page_params.item_per_page)
                .limit(page_params.item_per_page)
            )
            if filter_by_user_id:
                query = query.filter(Note.created_by == user_id)

            print("Total Item:", total_item)

            paginated_query = session.execute(query)
            paginated_query = paginated_query.scalars().all()

            notes = [NoteSchema.from_orm(p).__dict__ for p in paginated_query]

            meta = PaginationMetaResponse(
                total_item=total_item,
                page=page_params.page,
                item_per_page=page_params.item_per_page,
                total_page=math.ceil(total_item / page_params.item_per_page),
            )

            return notes, meta

class UpdateNote:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(self, user_id: int, note_id: int, request: UpdateNoteRequest) -> NoteSchema:
        with self.session as session:
            note = session.execute(
                select(Note).where(
                    (Note.note_id == note_id).__and__(Note.deleted_at == None)
                )
            )
            note = note.scalars().first()
            if not note:
                exception = HTTPException(description="note not found")
                exception.code = 404
                raise exception

            title_is_modified = note.title != request.title
            if title_is_modified:
                u = session.execute(
                    select(Note).where(Note.title == request.title)
                )
                u = u.scalars().first()
                if u is not None:
                    exception = HTTPException(description=f"title: {request.title} is already taken")
                    exception.code = 400
                    raise exception

            content_is_modified = note.content != request.content
            if content_is_modified:
                u = session.execute(
                    select(Note).where(Note.content == request.content)
                )
                u = u.scalars().first()
                if u is not None:
                    exception = HTTPException(description=f"email: {request.content} is already taken")
                    exception.code = 400
                    raise exception

            note.title = request.title
            note.content = request.content
            note.updated_at = datetime.datetime.utcnow()
            note.updated_by = user_id

            session.flush()
            return NoteSchema.from_orm(note)

class DeleteNote:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(self, user_id: int, note_id: int) -> NoteSchema:
        with self.session as session:
            note = session.execute(
                select(Note).where(
                    (Note.note_id == note_id).__and__(Note.deleted_at == None)
                )
            )
            note = note.scalars().first()
            if not note:
                exception = HTTPException(description="note not found")
                exception.code = 404
                raise exception

            note.deleted_at = datetime.datetime.utcnow()
            note.deleted_by = user_id

            session.flush()
            return NoteSchema.from_orm(note)