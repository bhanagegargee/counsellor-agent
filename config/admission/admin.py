import os
from django.contrib import admin, messages
from django.utils import timezone

from .models import PDFDocument
# from rag.ingest import ingest_pdf, remove_pdf_from_store


@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "is_indexed", "chunk_count", "indexed_at", "uploaded_at")
    list_filter = ("is_indexed",)
    readonly_fields = ("is_indexed", "chunk_count", "indexed_at", "uploaded_at")
    actions = ["index_selected_pdfs"]

    # Re-uploading a file means it needs indexing again
    def save_model(self, request, obj, form, change):
        if change and "file" in form.changed_data:
            from rag.ingest import remove_pdf_from_store
            remove_pdf_from_store(pdf_id=obj.pk)
            obj.is_indexed = False
            obj.chunk_count = 0
            obj.indexed_at = None
        super().save_model(request, obj, form, change)

    @admin.action(description="Index selected PDFs into vector store")
    def index_selected_pdfs(self, request, queryset):
        from rag.ingest import ingest_pdf
        for pdf in queryset:
            try:
                count = ingest_pdf(pdf.file.path, pdf.pk)
                pdf.is_indexed = True
                pdf.chunk_count = count
                pdf.indexed_at = timezone.now()
                pdf.save(update_fields=["is_indexed", "chunk_count", "indexed_at"])
                self.message_user(
                    request, f"'{pdf.title}': indexed {count} chunks.", messages.SUCCESS
                )
            except Exception as e:
                self.message_user(
                    request, f"'{pdf.title}' failed: {e}", messages.ERROR
                )

    # Keep the vector store in sync when PDFs are deleted
    def delete_model(self, request, obj):
        from rag.ingest import remove_pdf_from_store
        remove_pdf_from_store(pdf_id=obj.pk, source_file=os.path.basename(obj.file.name))
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        from rag.ingest import remove_pdf_from_store
        for obj in queryset:
            remove_pdf_from_store(pdf_id=obj.pk, source_file=os.path.basename(obj.file.name))
        super().delete_queryset(request, queryset)