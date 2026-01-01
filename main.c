//JSH v1.4
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <pwd.h>
#include <time.h>

typedef struct {
    char *args[16];
    int count;
} Command;

int main() {

    char input[256];

    while (1) {
        struct passwd *pw = getpwuid(geteuid());
        if (pw != NULL) {
            printf("\e[34m%s\e[35m@\e[31mJSH\e[35m:~\e[32m$\e[0m ", pw->pw_name);
        } else {
            perror("getpwuid failed");
        }   
        fgets(input, sizeof(input), stdin);

        Command cmd;
        cmd.count = 0;

        char *token = strtok(input, " \n");
        while (token != NULL && cmd.count < 16) {
            cmd.args[cmd.count++] = token;
            token = strtok(NULL, " \n");
        }
        cmd.args[cmd.count] = NULL;

        if (cmd.count == 0)
            continue;

        if (strcmp(cmd.args[0], "exit") == 0) { //exit cmd
            break;
        }
        else if (strcmp(cmd.args[0], "help") == 0) { //help cmd
            printf("any bash command also works!\nhelp - display this help message :)!\nexit - exit JSH\nver - list version and publication date\ncookie - play cookie clicker\nrps - play rock paper scissors\n");
        }
        else if (strcmp(cmd.args[0], "cookie") == 0) { //cookie clicker
            int cookies = 0;
            int clickers = 1;
            char buf[16];

            while (1) {

                printf("Cookies: %d\nClickers (cookies/click): %d\n", cookies, clickers);
                printf("Type 0 to exit back to JSH\nType 1 to buy another clicker for 5 cookies\nType 2 to click the cookie\n> ");

                fgets(buf, sizeof(buf), stdin);
                int inp = atoi(buf);

                if (inp == 0) {
                    break;
                }
                else if (inp == 1) {
                    if (cookies < 5) {
                        printf("Not enough cookies!\n");
                    } else {
                        cookies -= 5;
                        clickers++;
                    }
                }
                else if (inp == 2) {
                    cookies += clickers;
                }
                
            }
            
            continue;
        }
        else if (strcmp(cmd.args[0], "rps") == 0) { //rock... paper... scissors... shoot!
            while (1) {
                int usr;
                printf("0 for rock\n1 for paper\n2 for scissors\n3 to quit\n");
                scanf("%d", &usr);
                srand(time(NULL));
                int cpu = rand() % 3;
                if (cpu == 0) {
                    printf("I pick rock...\n");
                }
                else if (cpu == 1) {
                    printf("I pick paper...\n");
                }
                else if (cpu == 2) {
                    printf("I pick scissors...\n");
                }
                if (cpu == usr) {
                    printf("Tie!\n");
                }
                else if (cpu == 0 && usr == 1) {
                    printf("You win...\n");
                }
                else if (cpu == 0 && usr == 2) {
                    printf("I win!\n");
                }
                else if (cpu == 1 && usr == 0) {
                    printf("I win!\n");
                }
                else if (cpu == 1 && usr == 2) {
                    printf("You win...\n");
                }
                else if (cpu == 2 && usr == 0) {
                    printf("You win...\n");
                }
                else if (cpu == 2 && usr == 1) {
                    printf("I win!\n");
                }
                if (usr == 3) {
                    break;
                }
            }
        }
        else if (strcmp(cmd.args[0], "cd") == 0) { //cd
            if (cmd.count < 2) {
                fprintf(stderr, "cd: missing argument\n");
            } else {
                if (chdir(cmd.args[1]) != 0) {
                    perror("cd");
                }
            }
        }
        else if (strcmp(cmd.args[0], "ver") == 0) { //ver cmd, thats me btw, hi
            printf("James Shell v1.4 by James Baum published on December 8th 2025 with the MIT License");
        }
        else {
            pid_t pid = fork();

        if (pid < 0) {
            perror("fork failed");
            continue;
        }

        if (pid == 0) {
            // Child process
            execvp(cmd.args[0], cmd.args);
            perror("exec failed");
            exit(1);
        } 
        else {
            // Parent process
            int status;
            waitpid(pid, &status, 0);
        }
        }

    }

    return 0;
}
