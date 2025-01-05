from .models import Teacher, Subject, Timeslot, Department, TimeTable
from datetime import timedelta
import random

class TimetableScheduler:
    def __init__(self, departments, subjects, teachers, timeslots):
        self.departments = departments
        self.subjects = subjects
        self.teachers = teachers
        self.timeslots = timeslots
        self.population_size = 50
        self.generations = 100

    def generate_initial_population(self):
        population = []
        for _ in range(self.population_size):
            individual = []
            for department in self.departments:
                for subject in department.major_subjects.all() | department.minor_subjects.all():
                    timeslot = random.choice(self.timeslots)
                    teacher = random.choice(subject.assigned_teachers.all())
                    individual.append((department, subject, timeslot, teacher))
            population.append(individual)
        return population

    def fitness(self, individual):
        score = 0
        for department, subject, timeslot, teacher in individual:
            if is_teacher_available(teacher, timeslot):
                score += 1
            if is_teacher_under_working_hours(teacher, timeslot):
                score += 1
            if is_subject_under_lectures_per_week(subject):
                score += 1
            if is_duration_fits(timeslot, subject):
                score += 1
            if is_department_available(department, timeslot):
                score += 1
            if is_department_under_working_hours(department, timeslot):
                score += 1
            if is_department_under_lectures_per_week(department, subject):
                score += 1
            if is_subject_in_department(department, subject):
                score += 1
        return score

    def crossover(self, parent1, parent2):
        midpoint = len(parent1) // 2
        child = parent1[:midpoint] + parent2[midpoint:]
        return child

    def mutate(self, individual):
        mutation_rate = 0.1
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                department, subject, _, _ = individual[i]
                timeslot = random.choice(self.timeslots)
                teacher = random.choice(subject.assigned_teachers.all())
                individual[i] = (department, subject, timeslot, teacher)
        return individual

    def select_parents(self, population):
        population.sort(key=self.fitness, reverse=True)
        return population[:2]

    def generate_timetable(self):
        population = self.generate_initial_population()
        for _ in range(self.generations):
            new_population = []
            for _ in range(self.population_size):
                parent1, parent2 = self.select_parents(population)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
            population = new_population
        best_individual = max(population, key=self.fitness)
        return best_individual


def is_teacher_available(teacher, timeslot):
    return not TimeTable.objects.filter(subject__teachers=teacher, timeslot=timeslot).exists()

def is_teacher_under_working_hours(teacher, timeslot):
    total_working_minutes = int(teacher.working_hours) * 60
    total_scheduled_minutes = sum(
        timetable.subject.duration_per_lecture
        for timetable in TimeTable.objects.filter(subject__teachers=teacher)
    )
    current_duration = (timeslot.end_time - timeslot.start_time).total_seconds() / 60
    return total_scheduled_minutes + current_duration <= total_working_minutes

def is_subject_under_lectures_per_week(subject):
    total_lectures = TimeTable.objects.filter(subject=subject).count()
    return total_lectures < subject.lectures_per_week

def is_duration_fits(timeslot, subject):
    current_duration = (timeslot.end_time - timeslot.start_time).total_seconds() / 60
    return current_duration >= subject.duration_per_lecture

def is_department_available(department, timeslot):
    return not TimeTable.objects.filter(department=department, timeslot=timeslot).exists()

def is_department_under_working_hours(department, timeslot):
    total_scheduled_minutes = sum(
        timetable.subject.duration_per_lecture
        for timetable in TimeTable.objects.filter(department=department)
    )
    department_hours = (department.end_time - department.start_time).total_seconds() / 60
    current_duration = (timeslot.end_time - timeslot.start_time).total_seconds() / 60
    return total_scheduled_minutes + current_duration <= department_hours

def is_department_under_lectures_per_week(department, subject):
    total_major_lectures = TimeTable.objects.filter(department=department, subject__is_major=True).count()
    total_minor_lectures = TimeTable.objects.filter(department=department, subject__is_major=False).count()
    if subject.is_major:
        major_quota = department.total_lectures_per_week // 2
        return total_major_lectures < major_quota
    else:
        minor_quota = department.total_lectures_per_week // 2
        return total_minor_lectures < minor_quota

def is_subject_in_department(department, subject):
    if subject.is_major:
        return department.major_subjects.filter(pk=subject.pk).exists()
    else:
        return department.minor_subjects.filter(pk=subject.pk).exists()