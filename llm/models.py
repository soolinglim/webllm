from django.db import models

class UserInputInitial(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    session = models.UUIDField(blank=True, null=True, default=None)
    iteration = models.IntegerField(blank=True, null=True)
    user_input = models.TextField(blank=True)


class UserInput(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    session = models.UUIDField(blank=True, null=True, default=None)
    iteration = models.IntegerField(blank=True, null=True)
    user_input = models.TextField(blank=True)
    prompt = models.TextField(blank=True)
    response = models.TextField(blank=True)
    result = models.TextField(blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    elapsed_time = models.IntegerField(blank=True, null=True)
    version = models.IntegerField(blank=True, null=True)
    hide = models.BooleanField(default=False)


class ImagePrompt(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    session = models.UUIDField(blank=True, null=True, default=None)
    iteration = models.IntegerField(blank=True, null=True)
    instance = models.CharField(max_length=8, blank=True)
    user_input = models.TextField(blank=True)
    attributes = models.TextField(blank=True)
    response = models.TextField(blank=True)
    result = models.TextField(blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    elapsed_time = models.IntegerField(blank=True, null=True)


class Image(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    session = models.UUIDField(blank=True, null=True, default=None)
    iteration = models.IntegerField(blank=True, null=True)
    instance = models.CharField(max_length=8, blank=True)
    attributes = models.TextField(blank=True)
    prompt = models.TextField(blank=True)
    response = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    revised_prompt = models.TextField(blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    elapsed_time = models.IntegerField(blank=True, null=True)


class UserSelectionFeedback(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    session = models.UUIDField(blank=True, null=True, default=None)
    iteration = models.IntegerField(blank=True, null=True)
    parent1_id = models.CharField(max_length=8, blank=True)
    parent1_json = models.TextField(blank=True)
    parent1_image = models.URLField(blank=True, null=True)
    parent1_feedback = models.TextField(blank=True)
    parent2_id = models.CharField(max_length=8, blank=True)
    parent2_json = models.TextField(blank=True)
    parent2_image = models.URLField(blank=True, null=True)
    parent2_feedback = models.TextField(blank=True)
    current_iteration_results = models.TextField(blank=True)


class Crossover(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    session = models.UUIDField(blank=True, null=True, default=None)
    iteration = models.IntegerField(blank=True, null=True)
    parent1_id = models.CharField(max_length=8, blank=True)
    parent1 = models.TextField(blank=True)
    parent1_image = models.URLField(blank=True, null=True)
    parent2_id = models.CharField(max_length=8, blank=True)
    parent2 = models.TextField(blank=True)
    parent2_image = models.URLField(blank=True, null=True)
    prompt = models.TextField(blank=True)
    response = models.TextField(blank=True)
    result = models.TextField(blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    elapsed_time = models.IntegerField(blank=True, null=True)


class Mutation(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    session = models.UUIDField(blank=True, null=True, default=None)
    iteration = models.IntegerField(blank=True, null=True)
    attributes = models.TextField(blank=True)
    avoid_values = models.TextField(blank=True)
    prompt = models.TextField(blank=True)
    response = models.TextField(blank=True)
    result = models.TextField(blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    elapsed_time = models.IntegerField(blank=True, null=True)


class Children(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    session = models.UUIDField(blank=True, null=True, default=None)
    iteration = models.IntegerField(blank=True, null=True)
    children_after_crossover = models.TextField(blank=True)
    children_after_mutation = models.TextField(blank=True)


class FinalFeedback(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    session = models.UUIDField(blank=True, null=True, default=None)
    user_input = models.TextField(blank=True)
    iteration = models.IntegerField(blank=True, null=True)
    final_id = models.CharField(max_length=8, blank=True)
    final_json = models.TextField(blank=True)
    final_image = models.URLField(blank=True, null=True)
    final_feedback = models.TextField(blank=True)
    current_iteration_results = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    contact = models.TextField(blank=True)

