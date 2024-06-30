#include <stdio.h>

int getBoxNumber(int row, int col) {
    if (row < 3) {
        if (col < 3) {
            return 1;
        }
        if (col < 6) {
            return 2;
        }
        return 3;
    }
    if (row < 6) {
        if (col < 3) {
            return 4;
        }
        if (col < 6) {
            return 5;
        }
        return 6;
    }
    if (col < 3) {
        return 7;
    }
    if (col < 6) {
        return 8;
    }
    return 9;
}

int checkBox(int table[9][9], int boxNum, int num) {
    int row, col;
    if (boxNum <= 3) {
        row = 0;
    } else if (boxNum <= 6) {
        row = 3;
    } else {
        row = 6;
    }
    switch (boxNum) {
    case 1:
    case 4:
    case 7:
        col = 0;
        break;
    case 2:
    case 5:
    case 8:
        col = 3;
        break;
    case 3:
    case 6:
    case 9:
        col = 6;
        break;
    }
    for (int i = row; i < row + 3; i++) {
        for (int j = col; j < col + 3; j++) {
            if (table[i][j] == num) {
                return 0;
            }
        }
    }
    return 1;
}

int checkIfTableIsSolved(int table[9][9]) {
    for (int row = 0; row < 9; row++) {
        for (int col = 0; col < 9; col++) {
            if (table[row][col] == 0) {
                return 0;
            }
        }
    }
    return 1;
}

void printTable(int table[9][9]) {
    printf("|-----------------------|\n");
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            if ((j + 1) % 3 == 0) {
                printf("%d | ", table[i][j]);
            } else if (j == 0) {
                printf("| %d ", table[i][j]);
            } else {
                printf("%d ", table[i][j]);
            }
        }
        if ((i + 1) % 3 == 0) {
            printf("\n|-----------------------|\n");
        } else {
            printf("\n");
        }
    }
}

int backTracking(int table[9][9]) {
    if (checkIfTableIsSolved(table)) {
        return 1;
    }
    for (int row = 0; row < 9; row++) {
        for (int col = 0; col < 9; col++) {
            if (table[row][col] != 0) {
                continue;
            }
            for (int num = 1; num <= 9; num++) {
                int validNum = 1;
                // check row
                for (int i = 0; i < 9; i++) {
                    if (table[row][i] == num) {
                        validNum = 0;
                        break;
                    }
                }
                if (!validNum)
                    continue;
                // check col
                for (int i = 0; i < 9; i++) {
                    if (table[i][col] == num) {
                        validNum = 0;
                        break;
                    }
                }
                if (!validNum)
                    continue;
                // check box
                int boxNum = getBoxNumber(row, col);
                validNum = checkBox(table, boxNum, num);
                if (!validNum)
                    continue;
                table[row][col] = num;
                if (backTracking(table)) {
                    return 1;
                }
                table[row][col] = 0;
            }
            return 0;
        }
    }
    return 0;
}

int main() {
    int table[9][9] = {{0,0,6,0,7,1,0,3,0}, 
                       {0,0,0,0,4,0,0,7,0}, 
                       {0,0,0,0,5,6,9,0,0}, 
                       {0,1,0,0,0,4,0,5,0}, 
                       {0,8,0,0,3,0,0,0,0}, 
                       {7,0,0,5,0,0,6,0,0}, 
                       {0,6,8,0,2,0,0,0,0}, 
                       {0,4,2,9,0,0,0,0,7}, 
                       {0,9,7,0,0,3,5,0,0}};
    printTable(table);
    backTracking(table);
    printTable(table);
    return 0;
}