import subprocess
import click


@click.group()
def main():
    pass


@main.command()
def hello() -> None:
    """Show a little welcome message!"""
    print("Hello ! :wave:")


@main.command()
def launch() -> None:
    """Show a little welcome message!"""
    # cd /home/sebastien/github/CodinGame-thirdparty/GreenCircle
    # /usr/bin/env /usr/lib/jvm/java-8-openjdk-amd64/bin/java -cp /tmp/cp_7wdcdfymzs7kpssaoh0wot2cw.jar SkeletonMain 
    result = subprocess.run(["/usr/lib/jvm/java-8-openjdk-amd64/bin/java", "-cp", "/tmp/cp_7wdcdfymzs7kpssaoh0wot2cw.jar", "SkeletonMain", "Toto"], stdout=subprocess.PIPE)
    print(result)
    # score = int(result.stdout.decode('utf-8').splitlines()[-1])
    # print(score)
    # with open('log.txt', 'w') as f:
    #     f.write("\n".join(result.stdout.decode('utf-8').splitlines()[:-1]))

