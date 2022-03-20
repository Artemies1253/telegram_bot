from django.db import models


class ProblemStatement(models.Model):
    full_name = models.CharField(max_length=255)
    software_section = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Обращение {self.id} - от {self.full_name}"


class Photo(models.Model):
    problem_statement = models.ForeignKey(to=ProblemStatement, on_delete=models.CASCADE, related_name="files")
    instagram_file_id = models.CharField(max_length=255)

    def __str__(self):
        return f"Фотография {self.id} - {self.problem_statement}"
