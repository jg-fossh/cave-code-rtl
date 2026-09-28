/**
 * @file main.c
 * @brief Comprehensive demonstration of C programming language fundamentals.
 * Covers: Data types, Control Flow, Structures, Pointers, Dynamic Memory, 
 * Function Pointers, and File I/O.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

// 1. MACROS & CONSTANTS
#define MAX_NAME_LENGTH 50
#define SUCCESS 0
#define FAILURE -1

// 2. STRUCTURES & ENUMS
typedef enum {
    FRESHMAN,
    SOPHOMORE,
    JUNIOR,
    SENIOR
} YearLevel;

typedef struct {
    int id;
    char name[MAX_NAME_LENGTH];
    float gpa;
    YearLevel year;
} Student;

// 3. FUNCTION DECLARATIONS (PROTOTYPES)
void printStudentInfo(const Student *s);
bool updateGpa(Student *s, float new_gpa);
Student* createStudent(int id, const char *name, float gpa, YearLevel year);
void freeStudent(Student *s);
int saveStudentToFile(const Student *s, const char *filename);

// 4. MAIN ENTRY POINT
int main(void) {
    printf("=== C Comprehensive Features Demonstration ===\n\n");

    // --- Control Flow & Basic Data Types ---
    int total_students = 2;
    float running_gpa_sum = 0.0f;

    // --- Dynamic Memory Allocation & Pointers ---
    // Allocating an array of Student pointers
    Student **classroom = malloc(total_students * sizeof(Student*));
    if (classroom == NULL) {
        fprintf(stderr, "Memory allocation failed for classroom.\n");
        return FAILURE;
    }

    // Creating records using constructor-like function
    classroom[0] = createStudent(101, "Alice Smith", 3.85f, JUNIOR);
    classroom[1] = createStudent(102, "Bob Jones", 2.90f, FRESHMAN);

    // Verify allocations
    for (int i = 0; i < total_students; i++) {
        if (classroom[i] == NULL) {
            fprintf(stderr, "Failed to initialize student slot %d.\n", i);
            return FAILURE;
        }
    }

    // --- Using Pointers and Modifying Data ---
    printf("Initial Student Records:\n");
    for (int i = 0; i < total_students; i++) {
        printStudentInfo(classroom[i]);
    }

    printf("\nUpdating Bob's GPA...\n");
    // Passing by reference (pointer) to alter state
    if (updateGpa(classroom[1], 3.42f)) {
        printf("GPA successfully updated.\n");
    }

    // --- Math & Conditional Logic ---
    printf("\nUpdated Records & Analytics:\n");
    for (int i = 0; i < total_students; i++) {
        printStudentInfo(classroom[i]);
        running_gpa_sum += classroom[i]->gpa;
    }
    
    float average_gpa = running_gpa_sum / total_students;
    printf("Class Average GPA: %.2f\n", average_gpa);

    // --- File I/O Operations ---
    const char *db_file = "student_records.txt";
    printf("\nSaving %s's record to disk (%s)...\n", classroom[0]->name, db_file);
    if (saveStudentToFile(classroom[0], db_file) == SUCCESS) {
        printf("File persisted successfully.\n");
    } else {
        printf("Failed to save record.\n");
    }

    // --- Clean Up & Memory Deallocation ---
    for (int i = 0; i < total_students; i++) {
        freeStudent(classroom[i]); // Free individual student structs
    }
    free(classroom); // Free the pointer array wrapper
    classroom = NULL;

    printf("\nMemory cleaned up safely. Exiting program.\n");
    return SUCCESS;
}

// 5. FUNCTION DEFINITIONS

/**
 * Creates a Student instance safely on the Heap.
 */
Student* createStudent(int id, const char *name, float gpa, YearLevel year) {
    Student *new_student = malloc(sizeof(Student));
    if (new_student == NULL) {
        return NULL;
    }

    new_student->id = id;
    // Safely copy string limiting buffer bounds to prevent overflow
    strncpy(new_student->name, name, MAX_NAME_LENGTH - 1);
    new_student->name[MAX_NAME_LENGTH - 1] = '\0'; // Guarantee null-termination
    new_student->gpa = gpa;
    new_student->year = year;

    return new_student;
}

/**
 * Outputs student details to the console window.
 * Uses a pointer-to-const to protect data from accidental modification.
 */
void printStudentInfo(const Student *s) {
    if (s == NULL) return;

    const char *year_strings[] = {"Freshman", "Sophomore", "Junior", "Senior"};
    
    printf("ID: %d | Name: %-15s | GPA: %.2f | Year: %s\n", 
           s->id, s->name, s->gpa, year_strings[s->year]);
}

/**
 * Updates the GPA of a targeted student record with business rule validation.
 */
bool updateGpa(Student *s, float new_gpa) {
    if (s == NULL || new_gpa < 0.0f || new_gpa > 4.0f) {
        return false; // Guard clause against invalid ranges or null targets
    }
    s->gpa = new_gpa;
    return true;
}

/**
 * Safely writes structural entity properties down to a plain-text file.
 */
int saveStudentToFile(const Student *s, const char *filename) {
    if (s == NULL || filename == NULL) return FAILURE;

    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        perror("Error opening file");
        return FAILURE;
    }

    fprintf(file, "ID=%d\nName=%s\nGPA=%.2f\nYear=%d\n", 
            s->id, s->name, s->gpa, s->year);
    
    fclose(file); // Prevent resource leaks
    return SUCCESS;
}

/**
 * Frees dynamic memory and prevents dangling pointers.
 */
void freeStudent(Student *s) {
    if (s != NULL) {
        free(s);
    }
}
