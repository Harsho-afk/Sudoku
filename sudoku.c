#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct Table {
    int arr[9][9];
} TABLE;

typedef struct INDEX {
    int row;
    int col;
} INDEX;

void printTable(TABLE table) {
    printf("|-----------------------|\n");
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            if ((j + 1) % 3 == 0) {
                printf("%d | ", table.arr[i][j]);
            } else if (j == 0) {
                printf("| %d ", table.arr[i][j]);
            } else {
                printf("%d ", table.arr[i][j]);
            }
        }
        if ((i + 1) % 3 == 0) {
            printf("\n|-----------------------|\n");
        } else {
            printf("\n");
        }
    }
    printf("\n");
}

int checkIfTableIsSolved(TABLE table) {
    for (int row = 0; row < 9; row++) {
        for (int col = 0; col < 9; col++) {
            if (table.arr[row][col] == 0) {
                return 0;
            }
        }
    }
    return 1;
}

int checkIfValidMove(TABLE table, int row, int col, int num) {
    // check row and col
    for (int i = 0; i < 9; i++) {
        if (table.arr[row][i] == num) {
            return 0;
        }
        if (table.arr[i][col] == num) {
            return 0;
        }
    }
    // check box
    row = row - row % 3;
    col = col - col % 3;
    for (int i = row; i < row + 3; i++) {
        for (int j = col; j < col + 3; j++) {
            if (table.arr[i][j] == num) {
                return 0;
            }
        }
    }
    return 1;
}

int backTracking(TABLE *table) {
    if (checkIfTableIsSolved(*table)) {
        return 1;
    }
    for (int row = 0; row < 9; row++) {
        for (int col = 0; col < 9; col++) {
            if (table->arr[row][col] != 0) {
                continue;
            }
            for (int num = 1; num <= 9; num++) {
                if (!checkIfValidMove(*table, row, col, num)) {
                    continue;
                }
                table->arr[row][col] = num;
                if (backTracking(table)) {
                    return 1;
                }
                table->arr[row][col] = 0;
            }
            return 0;
        }
    }
    return 0;
}

void initTableToZero(TABLE *table) {
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            table->arr[i][j] = 0;
        }
    }
}

void copyTable(TABLE *dest, int src[9][9]) {
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            dest->arr[i][j] = src[i][j];
        }
    }
}

void getRandomValidTable(TABLE *table) {
    TABLE *gen = malloc(sizeof(TABLE));
    if (gen == NULL) {
        printf("Memory allocation failed.");
        exit(1);
    }
    initTableToZero(table);

    INDEX *availableIndex = malloc(sizeof(INDEX) * 9 * 9);
    if (availableIndex == NULL) {
        printf("Memory allocation failed.");
        free(gen);
        exit(1);
    }
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            availableIndex[(9 * i) + j].row = i;
            availableIndex[(9 * i) + j].col = j;
        }
    }

    int sizeOfAvailableIndex = 81;
    int sizeOfAvailableNumbers = 0;
    int rNum, row, col, rIndex;
    int *availableNumbers = NULL;
    srand(time(NULL));

    while (!checkIfTableIsSolved(*table)) {
        // get random index whose value is not 0
        rIndex = rand() % sizeOfAvailableIndex;
        while (table->arr[availableIndex[rIndex].row]
                         [availableIndex[rIndex].col] != 0) {
            rIndex = rand() % sizeOfAvailableIndex;
        }
        row = availableIndex[rIndex].row;
        col = availableIndex[rIndex].col;

        sizeOfAvailableNumbers = 0;
        if (availableNumbers != NULL)
            free(availableNumbers);
        availableNumbers = NULL;
        // find all the numbers which is valid in that index
        for (int num = 1; num <= 9; num++) {
            if (!checkIfValidMove(*table, row, col, num)) {
                continue;
            }
            table->arr[row][col] = num;
            copyTable(gen, table->arr);
            // printf("%d %d %d %d %d\n",
            // sizeOfAvailableIndex,sizeOfAvailableNumbers, row, col, num);
            if (backTracking(gen)) {
                // add the number to available numbers array
                int *tmp = realloc(availableNumbers,
                                   sizeof(int) * (sizeOfAvailableNumbers + 1));
                if (tmp == NULL) {
                    printf("Memory reallocation failed.");
                    free(gen);
                    free(availableIndex);
                    free(availableNumbers);
                    exit(1);
                } else {
                    availableNumbers = tmp;
                }
                availableNumbers[sizeOfAvailableNumbers] = num;
                sizeOfAvailableNumbers++;
            }
            table->arr[row][col] = 0;
        }

        // set that index to randomly chosen possible number
        if (sizeOfAvailableNumbers != 0) {
            rNum = availableNumbers[rand() % sizeOfAvailableNumbers];
            table->arr[row][col] = rNum;

            // remove that index from available index array
            for (int i = rIndex; i < sizeOfAvailableIndex - 1; i++) {
                availableIndex[i].row = availableIndex[i + 1].row;
                availableIndex[i].col = availableIndex[i + 1].col;
            }
            if (sizeOfAvailableIndex > 1) {
                INDEX *tmp = realloc(
                    availableIndex, sizeof(INDEX) * (sizeOfAvailableIndex - 1));
                if (tmp == NULL) {
                    printf("Memory reallocation failed.");
                    free(availableIndex);
                    free(gen);
                    free(availableNumbers);
                    exit(1);
                } else {
                    availableIndex = tmp;
                }
            }

            sizeOfAvailableIndex--;
        }
    }

    copyTable(table, gen->arr);
    free(availableIndex);
    free(gen);
    free(availableNumbers);
}

int main() {
    TABLE table;
    getRandomValidTable(&table);
    printTable(table);
    return 0;
}